from fastapi import FastAPI, HTTPException
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

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/status")
async def get_status():
    return {"status": "ok"}

@app.get("/echo")
async def echo(text: str):
    return {"echo": text}

@app.get("/predictions")
async def get_weather_predictions(location: str, prediction_date: date = Query(None)):
    if prediction_date:
        query = text("""
        SELECT date, location, prediction, accuracy
        FROM weather_predictions
        WHERE location = :location AND date = :prediction_date
        ORDER BY date DESC
        LIMIT 1;
        """)
        params = {'location': location, 'prediction_date': prediction_date}
    else:
        query = text("""
        SELECT date, location, prediction, accuracy
        FROM weather_predictions
        WHERE location = :location
        ORDER BY date DESC
        LIMIT 1;
        """)
        params = {'location': location}

    with mysql_engine.connect() as connection:
        result = connection.execute(query, params).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="No predictions found for the specified location and date")

    return WeatherPrediction(date=result[0], location=result[1], prediction=result[2], accuracy=result[3])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
