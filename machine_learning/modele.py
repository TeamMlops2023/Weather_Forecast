from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Charger le modèle pré-entraîné
model = joblib.load('model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Adaptez ces lignes pour correspondre aux caractéristiques attendues par votre modèle
    date = data.get('date')
    city = data.get('city')

    # Vous devez transformer 'date' et 'city' en un format numérique que votre modèle peut comprendre.
    # Ceci est juste un exemple. Vous devrez adapter cela en fonction de la façon dont votre modèle a été formé.
    model_input = [np.array([date, city])]

    prediction = model.predict(model_input)
    return jsonify({"result": prediction.tolist()})  # Convertit le résultat en liste pour la sérialisation JSON

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
