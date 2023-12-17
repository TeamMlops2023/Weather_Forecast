import logging
import pandas as pd
from fastapi import FastAPI, Query
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, generate_latest
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from elasticsearch import Elasticsearch

# Configuration du logging pour écrire dans un fichier spécifique.
logging.basicConfig(filename='modele_logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Création de l'instance FastAPI.
app = FastAPI()

# Configuration de l'instrumentation Prometheus pour exposer des métriques.
Instrumentator().instrument(app).expose(app)

# Compteur Prometheus pour suivre le nombre d'exécutions du modèle.
model_execution_counter = Counter('model_execution_count', 'Nombre d\'exécutions du modèle')

# Connexion à Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Chemin vers le fichier CSV contenant les données.
csv_file_path = 'data/data_features_with_location.csv'

@app.get("/")
def get_status():
    """ Point d'entrée de base pour vérifier que l'API est en ligne. """
    return "Bonjour et bienvenue !"

@app.get("/run_model")
def run_model():
    """ Exécute le modèle de prévision météorologique et renvoie les résultats. """
    # Incrémentation du compteur Prometheus à chaque exécution.
    model_execution_counter.inc()

    # Chargement des données à partir du fichier CSV.
    df = pd.read_csv(csv_file_path, index_col=0)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

    # Encodage des données catégorielles (les villes dans ce cas).
    le = LabelEncoder()
    df['location_encoded'] = le.fit_transform(df['location'])

    # Préparation des données pour l'entraînement du modèle.
    X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
    y = df['raintomorrow']
    dates = df['date']

    # Séparation en jeux d'entraînement et de test.
    X_train, X_test, y_train, y_test, dates_train, dates_test = train_test_split(X, y, dates, test_size=0.2, random_state=42)

    # Entraînement du modèle de forêt aléatoire.
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Prédiction sur le jeu de test.
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Création d'un DataFrame contenant les prédictions avec les dates correspondantes.
    predictions = pd.DataFrame({
        'Date': dates_test,
        'City': le.inverse_transform(X_test['location_encoded']),
        'Predicted': y_pred
    })
    rain_predictions = predictions[predictions['Predicted'] == 1].to_dict(orient='records')

    # Envoi des prédictions à Elasticsearch
    for prediction in rain_predictions:
        response = es.index(index="rain_predictions", document=prediction)
        logging.debug(f"Indexation response: {response}")

    # Retourne la précision et les prédictions de pluie au format JSON.
    return {
        "accuracy": accuracy,
        "rain_predictions": rain_predictions
    }

@app.get("/metrics")
def get_metrics():
    """ Expose les métriques pour Prometheus. """
    return generate_latest()

@app.get("/logs")
def read_logs(lines: int = Query(100, alias="lines")):
    """ Renvoie les dernières 'n' lignes du fichier de log. """
    log_file_path = 'modele_logs.log'
    if os.path.exists(log_file_path) and os.path.isfile(log_file_path):
        with open(log_file_path, 'r') as file:
            return "".join(file.readlines()[-lines:])
    else:
        return "Log file not found."
