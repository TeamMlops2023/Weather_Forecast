from fastapi import FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import date 
import os

# Récupérez les variables d'environnement pour la connexion à la base de données
mysql_url = os.environ.get('MYSQL_URL', 'database-service')
mysql_user = os.environ.get('MYSQL_USER', 'mlops')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'mlops')
database_name = 'mlops_weather'

# Créez l'URL de connexion à la base de données
connection_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_url}/{database_name}'

# Configuration de la connexion à la base de données
engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Modèle de données pour les résultats de la requête
class WeatherPrediction(BaseModel):
    id: int
    date: date
    location: str
    prediction: int
    accuracy: float

# Endpoint pour interroger la base de données
@app.get("/predictions/")
def get_weather_predictions():
    # Créez une session SQLAlchemy
    db = SessionLocal()

    # Exécutez une requête SQL pour récupérer les prédictions météo
    query = text("SELECT * FROM weather_predictions")
    results = db.execute(query).fetchall()

    # Transformez les résultats en liste de dictionnaires
    predictions = [dict(result) for result in results]

    # Fermez la session
    db.close()

    return predictions
