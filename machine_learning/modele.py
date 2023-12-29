from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Fonction pour charger les données et entraîner le modèle
def train_model():
    df = pd.read_csv('data/data_features_with_location.csv')
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    
    le = LabelEncoder()
    df['location_encoded'] = le.fit_transform(df['location'])
    
    X = df.drop(['raintomorrow', 'year', 'month', 'day', 'location', 'date'], axis=1)
    y = df['raintomorrow']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    return model, le

# Entraîner le modèle au démarrage du service
model, le = train_model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Convertissez 'date' et 'city' en entrée pour votre modèle ici
    # Par exemple, encodez la ville avec le LabelEncoder et traitez la date comme nécessaire
    city_encoded = le.transform([data['city']])
    # Préparez l'entrée du modèle en fonction de votre modèle spécifique

    prediction = model.predict([city_encoded])
    return jsonify({"result": prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
