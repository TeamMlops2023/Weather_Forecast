import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "FastAPI Service"}

@app.get("/run_model")
def run_model(date: str, city: str):
    # Interagir avec le service de Machine Learning
    ml_service_url = "http://ml-service:5000/predict"
    response = requests.post(ml_service_url, json={"date": date, "city": city})
    return response.json()
