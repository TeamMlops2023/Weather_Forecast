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

# Création de la connection à la base de données
# Variables de connexion
mysql_url = os.environ.get('MYSQL_URL')
mysql_user = 'root'
mysql_password = 'mysecretpassword'  # À compléter
database_name = 'mlops_weather'

# Création de l'URL de connexion
connection_url = 'mysql+pymysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# Création de la connexion
mysql_engine = create_engine(connection_url)

# Création de la classe de modèle pour la prédiction
class Prediction(BaseModel):
    date: datetime = None
    location: str = None
    prediction: int = None
    accuracy: float = None

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
@app.get('/prediction/{location:str}', response_model=Prediction)
async def get_prediction(location):
    date_format = "%Y-%m-%d"
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.strftime(date_format)

    with mysql_engine.connect() as connection:
        results = connection.execute(
            "SELECT date, location, prediction, accuracy FROM weather_predictions WHERE location = '{}' AND date = '{}';".format(location, tomorrow))

        result_list = [
            Prediction(
                date=i[0],
                location=i[1],
                prediction=i[2],
                accuracy=i[3]
            ) for i in results.fetchall()]

    if len(result_list) == 0:
        raise HTTPException(
            status_code=404,
            detail='Prédiction non trouvée')
    else:
        return result_list[0]

# Vérifie si le script est exécuté en tant que fichier principal
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
