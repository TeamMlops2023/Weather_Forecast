import logging
import pandas as pd
from fastapi import FastAPI, Query
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, generate_latest
from fastapi import FastAPI
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
import os
import uvicorn

# Configuration du logging pour écrire dans le fichier 'modele_logs.log'
logging.basicConfig(filename='modele_logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Création de l'application FastAPI
app = FastAPI()

# Instrumentation Prometheus
Instrumentator().instrument(app).expose(app)

# Compteur Prometheus
model_execution_counter = Counter('model_execution_count', 'Nombre d\'exécutions du modèle')

@app.get("/run_model")
def run_model():
    # Incrémenter le compteur à chaque appel de cette route
    model_execution_counter.inc()
    df = pd.read_csv("data/data_features_with_location.csv", index_col=0)

    # Convert 'year', 'month', 'day' to datetime
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

    # Encodage des villes
    le = LabelEncoder()
    df['location_encoded'] = le.fit_transform(df['location'])

    # Préparer les données pour le modèle
    X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
    y = df['raintomorrow']
    dates = df['date']

    # Séparation des données
    X_train, X_test, y_train, y_test, dates_train, dates_test = train_test_split(
        X, y, dates, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Préparation des prédictions avec les dates
    predictions = pd.DataFrame({
        'Date': dates_test,
        'City': le.inverse_transform(X_test['location_encoded']),
        'Predicted': y_pred
    })
    rain_predictions = predictions[(predictions['Predicted'] == 1)]

    return {"accuracy": accuracy, "rain_predictions": rain_predictions.to_dict(orient='records')}

@app.get("/metrics")
def get_metrics():
    return generate_latest()

@app.get("/logs")
def read_logs(lines: int = Query(100, alias="lines")):
    """
    Lire les dernières 'n' lignes du fichier de log.
    :param lines: Nombre de lignes de log à retourner.
    :return: Les dernières 'n' lignes du fichier de log.
    """
    log_file_path = 'modele_logs.log'
    if os.path.exists(log_file_path) and os.path.isfile(log_file_path):
        with open(log_file_path, 'r') as file:
            all_lines = file.readlines()
            # Récupérer les dernières 'n' lignes
            return "".join(all_lines[-lines:])
    else:
        return "Log file not found."


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
