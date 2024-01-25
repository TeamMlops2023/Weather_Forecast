from fastapi import FastAPI, Query, HTTPException
import uvicorn
from pydantic import BaseModel
from sqlalchemy.engine import create_engine
from datetime import datetime, timedelta
import os
from prometheus_fastapi_instrumentator import Instrumentator

# Création d'une instance FastAPI
app = FastAPI()

# Instrumentation pour Prometheus
Instrumentator().instrument(app).expose(app)

# Création de la connexion à la base de données
# Variables de connexion
mysql_url = os.environ.get('MYSQL_URL', 'database-service')  # Utilisez le nom du service Kubernetes comme hôte par défaut
mysql_user = os.environ.get('MYSQL_USER', 'mlops')           # Utilisateur par défaut 'mlops'
mysql_password = os.environ.get('MYSQL_PASSWORD', 'mlops')   # Mot de passe par défaut 'mlops'
database_name = 'mlops_weather'

# Création de l'URL de connexion
connection_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_url}/{database_name}'

# Création de la connexion
mysql_engine = create_engine(connection_url)

# Création de la classe de modèle pour la prédiction
class Prediction(BaseModel):
    date: datetime
    location: str
    prediction: int
    accuracy: float

# Définition de l'endpoint racine ("/")
@app.get("/")
async def read_root():
    return {"Hello": "World"}

# Définition de l'endpoint "/status"
@app.get("/status")
async def get_status():
    return {"status": "ok"}

# Définition de l'endpoint "/echo" avec un paramètre de requête textuel
@app.get("/echo")
async def echo(text: str = Query(None, min_length=1, max_length=100)):
    return {"echo": text}

# Définition de l'endpoint "/prediction" avec un paramètre de requête textuel
@app.get('/prediction/{location}', response_model=Prediction)
async def get_prediction(location: str):
    date_format = "%Y-%m-%d"
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.strftime(date_format)

    with mysql_engine.connect() as connection:
        results = connection.execute(
            "SELECT date, location, prediction, accuracy FROM weather_predictions WHERE location = %s AND date = %s;",
            (location, tomorrow)
        )
        result_list = [
            Prediction(
                date=i[0],
                location=i[1],
                prediction=i[2],
                accuracy=i[3]
            ) for i in results.fetchall()
        ]

    if not result_list:
        raise HTTPException(
            status_code=404,
            detail='Prediction not found'
        )
    return result_list[0]

# Vérifie si le script est exécuté en tant que fichier principal
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
