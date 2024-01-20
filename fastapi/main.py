from fastapi import FastAPI, Query
from prometheus_client import start_http_server, Counter

# Création d'une instance FastAPI
app = FastAPI()

# Définition d'une métrique Prometheus pour compter les requêtes
request_counter = Counter('fastapi_requests_total', 'Total number of requests to FastAPI')

# Définition de l'endpoint racine ("/")
@app.get("/")
def read_root():
    # Incrémente la métrique pour chaque requête reçue
    request_counter.inc()
    
    # Renvoie un message JSON lorsque quelqu'un accède à la racine de l'application
    return {"Hello": "World"}

# Définition de l'endpoint "/status"
@app.get("/status")
def get_status():
    # Incrémente la métrique pour chaque requête reçue
    request_counter.inc()
    
    # Renvoie un statut JSON "ok" lorsque quelqu'un accède à la route "/status"
    return {"status": "ok"}

# Définition de l'endpoint "/echo" avec un paramètre de requête textuel
@app.get("/echo")
def echo(text: str = Query(None, min_length=1, max_length=100)):
    # Incrémente la métrique pour chaque requête reçue
    request_counter.inc()
    
    # Valide le paramètre de requête et le renvoie dans une réponse JSON
    return {"echo": text}

# Faire la prédiction
# (Assurez-vous que cette partie est correctement instrumentée pour collecter des métriques)

# Démarrer un serveur HTTP Prometheus pour exposer les métriques
if __name__ == "__main__":
    # Démarrer le serveur Prometheus sur le port 8000
    start_http_server(8000)

    # Exécute l'application en utilisant Uvicorn avec les paramètres spécifiés
    uvicorn.run("main:app", host="0.0.0.0", port=8001, log_level="debug")
