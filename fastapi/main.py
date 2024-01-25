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

# Création de la connection à la base sql
# Variable de connection
mysql_url = os.environ.get('MYSQL_URL')
mysql_user = 'root'
mysql_password = 'mysecretpassword'  # to complete
database_name = 'mlops_weather'

# Création de l'URL de connection
connection_url = 'mysql+pymysql://{user}:{password}@{url}/{database}'.format(
    user=mysql_user,
    password=mysql_password,
    url=mysql_url,
    database=database_name
)

# Création de la connection
mysql_engine = create_engine(connection_url)

# creation de la classe prediction
class predict(BaseModel):
    date: datetime = 99991231
    ville: str = 'paris'
    prediction: str = 'ne sait pas'
    proba: float = 0.5

# Définition de l'endpoint racine ("/")
@app.get("/")
async def read_root():
    # Renvoie un message JSON lorsque quelqu'un accède à la racine de l'application
    return {"Hello": "World"}

# Définition de l'endpoint "/status"
@app.get("/status")
async def get_status():
    # Renvoie un statut ok = 1
    return 1

# Définition de l'endpoint "/prediction" avec un paramètre de requête textuel
@app.get('/prediction/{ville:str}', response_model=predict)
async def get_prediction(ville):
    date_format = "%Y%m%d"
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow = tomorrow.strftime(date_format)

    with mysql_engine.connect() as connection:
        results = connection.execute(
            'SELECT * FROM weather_predictions WHERE weather_predictions.ville = "{}" AND weather_predictions.date = "{}";'.format(ville, tomorrow))

    results = [
        predict(
            date = i[0],
            ville = i[1],
            prediction = i[2],
            proba = i[3]
            ) for i in results.fetchall()]

    if len(results) == 0:
        raise HTTPException(
            status_code=404,
            detail='Prédiction non trouvée')
    else:
        return results[0]

# Vérifie si le script est exécuté en tant que fichier principal
if __name__ == "__main__":
    # Exécute l'application en utilisant Uvicorn avec les paramètres spécifiés
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
