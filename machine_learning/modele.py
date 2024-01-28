import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import mysql.connector
from mysql.connector import Error
import os
import time
from prometheus_client import start_http_server, Summary, Gauge

# Définir des métriques Prometheus
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
MODEL_ACCURACY = Gauge('model_accuracy', 'Accuracy of the ML model')

# Démarrer le serveur de métriques pour Prometheus sur le port 8000
start_http_server(8000)
print("Server for Prometheus metrics started on port 8000.")

# Récupération de la variable d'environnement indiquant l'environnement actuel
environment = os.environ.get("ML_ENVIRONMENT", "test")
print(f"Sending data to the environment: {environment}")

# Attente avant de commencer, pour s'assurer que la base de données est prête
print("Waiting for 20 seconds before starting...")
time.sleep(20)

# Tentatives de connexion à la base de données
max_attempts = 5
attempt_count = 0

while attempt_count < max_attempts:
    try:
        print(f"Attempting to connect to the database, try {attempt_count + 1}")
        db = mysql.connector.connect(
            host="database-service",
            user="root",
            password="mysecretpassword",
            database="mlops_weather"
        )
        print("Connected to MySQL")
        cursor = db.cursor()
        break
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        attempt_count += 1
        time.sleep(5)

if attempt_count == max_attempts:
    print("Failed to connect to MySQL after several attempts")
    exit(1)

# Chemin vers le fichier de données
data_file_path = 'data/data_features_with_location.csv'
print(f"Loading data from {data_file_path}")

# Chargement des données
df = pd.read_csv(data_file_path)
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
print("Data loaded successfully.")

# Encodage des variables catégorielles
le = LabelEncoder()
df['location_encoded'] = le.fit_transform(df['location'])
print("Categorical variables encoded.")

# Préparation des données pour l'entraînement
X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
y = df['raintomorrow']

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Data split into training and test sets.")

# Entraînement du modèle et suivi du temps de traitement
with REQUEST_TIME.time():
    model = RandomForestClassifier()
    print("Starting model training...")
    model.fit(X_train, y_train)
    print("Model trained.")

    # Mise à jour de la métrique de précision
    accuracy = model.score(X_test, y_test)
    MODEL_ACCURACY.set(accuracy)
    print(f"Model accuracy: {accuracy}")

# Prédiction et insertion dans la base de données
try:
    for i in range(len(predictions)):
        date = df.iloc[i]['date']
        location = df.iloc[i]['location']
        prediction = predictions[i].item()

        check_query = "SELECT EXISTS(SELECT 1 FROM weather_predictions WHERE date=%s AND location=%s)"
        cursor.execute(check_query, (date, location))
        exists = cursor.fetchone()[0]

        if not exists:
            insert_query = "INSERT INTO weather_predictions (date, location, prediction, accuracy) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (date, location, prediction, accuracy))
            db.commit()
            print(f"Prediction inserted for {date} and {location}.")
        else:
            print(f"Entry for {date} and {location} already exists.")
except Error as e:
    print(f"SQL Error: {e}")
finally:
    # Fermeture de la connexion à la base de données
    if db.is_connected():
        cursor.close()
        db.close()
        print("Database connection closed.")

print("Predictions successfully made and recorded in the database.")
