import pandas as pd
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

def load_and_train_model():
    df = pd.read_csv('data/data_features_with_location.csv', index_col=0)
    # ... (Code pour entraîner le modèle)
    return model, le

model, le = load_and_train_model()

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    date = data['date']
    city = data['city']
    # Prédiction basée sur le modèle
    # ...
    prediction = {"result": "prediction_result"}
    return jsonify(prediction)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
