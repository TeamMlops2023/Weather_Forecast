from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from datetime import date
import os

app = FastAPI()

# Adresse IP du conteneur MySQL
mysql_ip = '10.96.39.152'  # Utilisez l'adresse IP de votre conteneur MySQL

# Variables de connexion à la base de données
mysql_user = os.environ.get('MYSQL_USER', 'mlops')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'mlops')
database_name = 'mlops_weather'

# Création de l'URL de connexion
connection_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_ip}/{database_name}'

# Création de la connexion
mysql_engine = create_engine(connection_url)

class WeatherPrediction(BaseModel):
    date: date
    location: str
    prediction: int
    accuracy: float

@app.get("/predictions")
async def get_weather_predictions(location: str, prediction_date: date = None):
    # Construire la requête de base
    query = text("""
    SELECT date, location, prediction, accuracy
    FROM weather_predictions
    WHERE location = :location
    """)

    # Ajouter une clause conditionnelle pour la date si elle est fournie
    if prediction_date:
        query = text(f"{query} AND date = :prediction_date")

    query = text(f"{query} ORDER BY date DESC LIMIT 1;")

    # Préparer les paramètres pour la requête SQL
    params = {'location': location}
    if prediction_date:
        params['prediction_date'] = prediction_date

    with mysql_engine.connect() as connection:
        result = connection.execute(query, params).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="No predictions found for the specified location and date")

    return WeatherPrediction(date=result[0], location=result[1], prediction=result[2], accuracy=result[3])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
