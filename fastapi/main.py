from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import date
import os

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
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)


class WeatherPrediction(BaseModel):
    id: int
    date: date
    location: str
    prediction: int
    accuracy: float


@app.get("/predictions/")
def get_weather_predictions():
    # Créez une session SQLAlchemy
    db = SessionLocal()

    try:
        # Exécutez une requête SQL pour récupérer les prédictions météo
        query = text("SELECT * FROM weather_predictions")
        results = db.execute(query).fetchall()

        # Transformez les résultats en liste de dictionnaires
        predictions = [dict(result) for result in results]

        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        # Fermez la session
        db.close()
