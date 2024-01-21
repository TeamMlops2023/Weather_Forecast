from fastapi import FastAPI, Query
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator

# Création d'une instance FastAPI
app = FastAPI()

# Instrumentation pour Prometheus
Instrumentator().instrument(app).expose(app)

# Définition de l'endpoint racine ("/")
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Définition de l'endpoint "/status"
@app.get("/status")
def get_status():
    return {"status": "ok"}

# Définition de l'endpoint "/echo" avec un paramètre de requête textuel
@app.get("/echo")
def echo(text: str = Query(None, min_length=1, max_length=100)):
    return {"echo": text}

# Vérifie si le script est exécuté en tant que fichier principal
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
