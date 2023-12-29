from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/run_model")
def run_model(date: str, city: str):
    # Préparer les données pour le modèle ML
    data = {
        "date": date,
        "city": city
    }

    # Envoyer les données au service ML et obtenir la réponse
    response = requests.post("http://ml-service:5000/predict", json=data)
    return response.json()
