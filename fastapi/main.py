from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from datetime import date
import os

app = FastAPI()

# Adresse IP du conteneur MySQL (remplacez par l'adresse IP appropriée)
mysql_ip = '10.96.39.152'  # Remplacez ceci par l'adresse IP de votre conteneur MySQL

# Variables de connexion à la base de données
mysql_user = os.environ.get('MYSQL_USER', 'mlops')
mysql_password = os.environ.get('MYSQL_PASSWORD', 'mlops')
database_name = 'mlops_weather'

# Création de l'URL de connexion en utilisant l'adresse IP
connection_url = f'mysql+pymysql://{mysql_user}:{mysql_password}@{mysql_ip}/{database_name}'

# Création de la connexion
mysql_engine = create_engine(connection_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

class WeatherPrediction(BaseModel):
    id: int
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
async def echo(text: str = Query(None, min_length=1, max_length=100)):
    return {"echo": text}

@app.get("/predictions/")
def get_weather_predictions(location: str, date: date):
    db = SessionLocal()

    try:
        query = text("""
    SELECT date, location, prediction, accuracy
    FROM weather_predictions
    WHERE location = :location
    ORDER BY date DESC
    LIMIT 1;
""")
        results = db.execute(query, {'location': location, 'date': date}).fetchall()

        predictions = [dict(result) for result in results]
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
