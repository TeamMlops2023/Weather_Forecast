from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/run_model")
def run_model(date: str, city: str):
    # Structurer les données pour le modèle ML
    data_to_send = {
        "Date": date,
        "City": city
    }

    # Remplacer l'URL ci-dessous par l'URL réelle de votre service ML
    ml_service_url = "http://ml-service:5000/predict"
    
    try:
        # Envoyer les données au service ML et obtenir la réponse
        response = requests.post(ml_service_url, json=data_to_send)
        response.raise_for_status()  # Cela va déclencher une exception si la requête échoue
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=str(e))
