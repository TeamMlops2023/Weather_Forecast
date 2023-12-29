from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Charger les données et entraîner le modèle
def load_and_train_model():
    df = pd.read_csv('data/data_features_with_location.csv', index_col=0)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    le = LabelEncoder()
    df['location_encoded'] = le.fit_transform(df['location'])
    X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
    y = df['raintomorrow']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model, le

model, le = load_and_train_model()

@app.route('/predict', methods=['POST'])
def predict():
    # Récupérer les données de la requête POST
    data = request.get_json(force=True)
    
    # Traitement des données (ex: conversion des dates et des villes en caractéristiques numériques)
    # ...
    # Vous devrez adapter cette partie en fonction de la manière dont votre modèle s'attend à recevoir les données
    date = pd.to_datetime(data["date"])
    city = le.transform([data["city"]])
    model_input = ...  # Créez ici le format d'entrée attendu par votre modèle

    # Effectuer la prédiction
    prediction = model.predict(model_input)

    # Créer la réponse
    response = {
        "Date": data["date"],
        "City": data["city"],
        "Predicted": int(prediction[0])  # Convertir la prédiction en un format approprié
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
