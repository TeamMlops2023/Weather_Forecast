import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import mysql.connector
from mysql.connector import Error
import os
import time

# Récupérez la variable d'environnement qui indique l'environnement actuel
environment = os.environ.get("ML_ENVIRONMENT", "test")  # Par défaut, c'est "test" si la variable n'est pas définie

# Pause pendant 20 secondes pour s'assurer que la base de données est prête
print("Attente de 20 secondes avant de commencer...")
time.sleep(20)

# Paramètres de réessai de connexion
max_attempts = 5
attempt_count = 0

while attempt_count < max_attempts:
    try:
        print(f"Tentative de connexion à la base de données, essai {attempt_count + 1}")
        db = mysql.connector.connect(
            host="database-service",
            user="root",
            password="mysecretpassword",
            database="mlops_weather"
        )
        print("Connecté à MySQL")
        cursor = db.cursor()
        break
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
        attempt_count += 1
        time.sleep(5)

if attempt_count == max_attempts:
    print("Échec de la connexion à MySQL après plusieurs tentatives")
    exit(1)

# Chemin vers le fichier de données
chemin_fichier_donnees = 'data/data_features_with_location.csv'
print(f"Chargement des données depuis {chemin_fichier_donnees}")

# Charger les données
df = pd.read_csv(chemin_fichier_donnees)
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
print("Données chargées avec succès.")

# Encodage des variables catégorielles
le = LabelEncoder()
df['location_encoded'] = le.fit_transform(df['location'])
print("Variables catégorielles encodées.")

# Préparation des données pour l'entraînement
X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
y = df['raintomorrow']

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print("Données séparées en ensembles d'entraînement et de test.")

# Entraînement du modèle
model = RandomForestClassifier()
print("Début de l'entraînement du modèle...")
model.fit(X_train, y_train)
print("Modèle entraîné.")

# Prédiction
predictions = model.predict(X_test)
print("Prédictions réalisées.")

# Insertion des prédictions dans la base de données
try:
    for i in range(len(predictions)):
        date = df.iloc[i]['date']
        location = df.iloc[i]['location']
        prediction = predictions[i].item()
        accuracy = model.score(X_test, y_test)

        check_query = "SELECT EXISTS(SELECT 1 FROM weather_predictions WHERE date=%s AND location=%s)"
        cursor.execute(check_query, (date, location))
        exists = cursor.fetchone()[0]

        if not exists:
            insert_query = "INSERT INTO weather_predictions (date, location, prediction, accuracy) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (date, location, prediction, accuracy))
            db.commit()  # Commit après chaque insertion réussie
            print(f"Insertion de la prédiction pour {date} et {location}.")
        else:
            print(f"Entrée pour {date} et {location} existe déjà.")
except Error as e:
    print(f"Erreur SQL : {e}")

finally:
    # Fermeture de la connexion à la base de données
    if db.is_connected():
        cursor.close()
        db.close()
        print("Connexion à la base de données fermée.")

print("Prédictions effectuées avec succès et enregistrées dans la base de données.")
