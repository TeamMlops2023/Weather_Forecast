from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Charger le modèle pré-entraîné
model = joblib.load('model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    # Transformez 'data' en format approprié pour le modèle
    # Par exemple :
    model_input = [data['feature1'], data['feature2'], ...]
    prediction = model.predict([model_input])
    return jsonify({"result": prediction})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
