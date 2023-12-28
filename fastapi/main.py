from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/run_model")
def run_model():
    # Exemple de requête au service ML
    response = requests.post("http://ml-service:5000/predict", json={"data": "your_data"})
    return response.json()
