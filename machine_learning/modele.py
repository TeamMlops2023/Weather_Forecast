from flask import Flask, request, jsonify
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Charger le modèle pré-entraîné
model, le = joblib.load('model_with_encoder.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    date = data['date']
    city = data['city']

    # Convertir la date en format datetime
    date = pd.to_datetime(date, format='%Y-%m-%d')

    # Préparer les données pour le modèle
    # (Cela doit correspondre à la manière dont vous avez formé votre modèle)
    model_input = pd.DataFrame({
        'year': [date.year],
        'month': [date.month],
        'day': [date.day],
        'location_encoded': le.transform([city])
    })

    # Faire la prédiction
    prediction = model.predict(model_input)
    return jsonify({"prediction": int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
