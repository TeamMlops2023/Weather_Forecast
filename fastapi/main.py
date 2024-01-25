from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.engine import create_engine
from datetime import datetime
from datetime import date
import os
from prometheus_fastapi_instrumentator import Instrumentator

# Création d'une instance FastAPI
app = FastAPI()

# Instrumentation pour Prometheus
Instrumentator().instrument(app).expose(app)

# Variables de connexion à la base de données
mysql_url = os.environ.get('MYSQL_URL', 'database-service')
mysql_user = os.environ.get('MYSQL_USER', 'mlops')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'mlops')
database_name = 'mlops_weather'

# Création de l'URL de connexion
connection_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_url}/{database_name}'

# Création de la connexion
mysql_engine = create_engine(connection_url)

# Modèle pour les prédictions
class Prediction(BaseModel):
    date: date
    location: str
    prediction: int
    accuracy: float

# Modèle pour les données historiques
class HistoricalData(BaseModel):
    date: datetime
    location: str
    status: int
    value: float

# Endpoint racine
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Endpoint pour vérifier le statut
@app.get("/status")
async def get_status():
    return {"status": "ok"}

# Endpoint pour l'écho
@app.get("/echo")
async def echo(text: str = Query(None, min_length=1, max_length=100)):
    return {"echo": text}

# Nouvelle route pour obtenir les données historiques
@app.get("/historical-data")
async def get_historical_data(location: str, start_date: date, end_date: date):
    with mysql_engine.connect() as connection:
        query = """
                SELECT date, location, status, value 
                FROM historical_weather_data 
                WHERE location = %s AND date BETWEEN %s AND %s;
                """
        results = connection.execute(query, (location, start_date, end_date))
        data = [HistoricalData(date=row[0], location=row[1], status=row[2], value=row[3]) for row in results.fetchall()]

    if not data:
        raise HTTPException(status_code=404, detail="No historical data found")

    return data

# Exécuter l'application si c'est le fichier principal
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
