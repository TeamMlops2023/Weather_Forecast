import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import mysql.connector
from mysql.connector import Error
import time

# Pause pendant 20 secondes
time.sleep(20)

# Paramètres de réessai de connexion
max_attempts = 5
attempt_count = 0

while attempt_count < max_attempts:
    try:
        # Connexion à la base de données
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
        time.sleep(5)  # Attendre 5 secondes avant de réessayer

if attempt_count == max_attempts:
    print("Échec de la connexion à MySQL après plusieurs tentatives")
    exit(1)

# Chemin vers le fichier de données
chemin_fichier_donnees = os.path.join('data', 'data_features_with_location.csv')

# Charger les données
df = pd.read_csv(chemin_fichier_donnees)
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])

# Encodage des variables catégorielles
le = LabelEncoder()
df['location_encoded'] = le.fit_transform(df['location'])

# Préparation des données pour l'entraînement
X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
y = df['raintomorrow']

# Séparation des données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraînement du modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Prédiction
predictions = model.predict(X_test)

# Insertion des prédictions dans la base de données
for i in range(len(predictions)):
    date = df.iloc[i]['date']
    location = df.iloc[i]['location']
    prediction = predictions[i].item()
    accuracy = model.score(X_test, y_test)  # Calcul de l'exactitude du modèle

    # Vérification si l'entrée existe déjà
    check_query = "SELECT EXISTS(SELECT 1 FROM weather_predictions WHERE date=%s AND location=%s)"
    cursor.execute(check_query, (date, location))
    exists = cursor.fetchone()[0]

    if not exists:
        insert_query = "INSERT INTO weather_predictions (date, location, prediction, accuracy) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (date, location, prediction, accuracy))
    else:
        print(f"Entrée pour {date} et {location} existe déjà.")

# Commit des modifications dans la base de données
db.commit()

# Fermeture de la connexion à la base de données
cursor.close()
db.close()

# Affichage des prédictions
print(predictions)
