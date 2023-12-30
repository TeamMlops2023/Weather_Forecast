import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os
import mysql.connector  # Importez le module MySQL

# Connexion à la base de données MySQL
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="mysecretpassword",
    database="mlops_weather"
)

# Créez un curseur pour exécuter des requêtes SQL
cursor = db.cursor()

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

# Insertion des prédictions dans la base de données au fur et à mesure qu'elles sont générées
for i in range(len(predictions)):
    date = df.iloc[i]['date']
    city = df.iloc[i]['location']
    predicted = predictions[i]
    accuracy = 0.8864667858616422  # Remplacez par votre valeur d'exactitude réelle
    insert_query = "INSERT INTO model_predictions (Date, City, Predicted, Accuracy) VALUES (%s, %s, %s, %s)"
    cursor.execute(insert_query, (date, city, predicted, accuracy))

# Commit des modifications dans la base de données
db.commit()

# Fermeture de la connexion à la base de données
db.close()

# Affichage des prédictions
print(predictions)
