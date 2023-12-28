from flask import Flask, request, jsonify
import pandas as pd
# Importez et configurez votre modèle ML ici

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    # Effectuez la prédiction en utilisant votre modèle ML
    # Exemple: prediction = model.predict(data)
    return jsonify({"prediction": "result"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
