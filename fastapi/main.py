from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from datetime import date
import os

# Création d'une instance FastAPI
app = FastAPI()

# Variables de connexion à la base de données
mysql_url = os.environ.get('MYSQL_URL', 'database-service')
mysql_user = os.environ.get('MYSQL_USER', 'mlops')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'mlops')
database_name = 'mlops_weather'

# Création de l'URL de connexion
connection_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_url}/{database_name}'

# Création de la connexion
mysql_engine = create_engine(connection_url)

# Modèle pour les données historiques
class HistoricalData(BaseModel):
    date: date
    location: str
    prediction: int
    accuracy: float

# Endpoint pour obtenir les données historiques d'une ville
@app.get("/predictions")
async def get_predictions(city: str):
    query = text("""
        SELECT date, location, prediction, accuracy 
        FROM weather_predictions 
        WHERE location = :city
        ORDER BY date DESC
        LIMIT 1;
    """)
    
    with mysql_engine.connect() as connection:
        result = connection.execute(query, {'city': city}).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="No predictions found for the city")

    return HistoricalData(date=result[0], location=result[1], prediction=result[2], accuracy=result[3])

# Exécuter l'application si c'est le fichier principal
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
