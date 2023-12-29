from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

# Fonction pour charger les données et entraîner le modèle
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
    data = request.get_json(force=True)
    # Adaptez cette partie pour accepter la date et la ville en entrée
    # Exemple : date = data['date'], city = data['city']
    # Transformez ces entrées en un format approprié pour votre modèle
    # Par exemple, encodez la ville avec le LabelEncoder

    # Ici, vous devez ajouter la logique pour transformer 'date' et 'city' en entrée pour votre modèle

    # Effectuez la prédiction
    prediction = model.predict([model_input])
    return jsonify({"result": prediction})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
