from fastapi import FastAPI, Query
import uvicorn
from prometheus_fastapi_instrumentator import Instrumentator, metrics

# Création d'une instance FastAPI
app = FastAPI()

# Configurez l'instrumentation Prometheus
Instrumentator().instrument(app).expose(app)

# Définition de l'endpoint racine ("/")
@app.get("/")
def read_root():
    # Renvoie un message JSON lorsque quelqu'un accède à la racine de l'application
    return {"Hello": "World"}

# Définition de l'endpoint "/status"
@app.get("/status")
def get_status():
    # Renvoie un statut JSON "ok" lorsque quelqu'un accède à la route "/status"
    return {"status": "ok"}

# Définition de l'endpoint "/echo" avec un paramètre de requête textuel
@app.get("/echo")
def echo(text: str = Query(None, min_length=1, max_length=100)):
    # Valide le paramètre de requête et le renvoie dans une réponse JSON
    return {"echo": text}

# Ajoutez une route pour exporter les métriques Prometheus au chemin "/metrics"
@app.get("/metrics")
async def get_metrics():
    return metrics()

# Vérifie si le script est exécuté en tant que fichier principal
if __name__ == "__main__":
    # Exécute l'application en utilisant Uvicorn avec les paramètres spécifiés
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
