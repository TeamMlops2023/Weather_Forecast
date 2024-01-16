from fastapi import FastAPI
import uvicorn
import joblib

app = FastAPI()

# Charger le modèle entraîné
model = joblib.load("/app/data/modele_entraîné.pkl")

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

@app.post("/predict")
async def predict(request: Request):
    # Récupérer les données de la requête
    data = await request.json()
    
    # Supposons que data est un dictionnaire qui contient les données nécessaires pour votre modèle
    # Par exemple: data = {"feature1": value1, "feature2": value2, ...}
    
    # Convertir les données en format approprié pour votre modèle
    # Par exemple, si votre modèle attend un DataFrame pandas
    # input_data = pd.DataFrame([data])
    
    # Faire la prédiction
    prediction = model.predict(input_data)

    # Renvoyer la prédiction
    return {"prediction": prediction.tolist()}

# Vérifie si le script est exécuté en tant que fichier principal
if __name__ == "__main__":
    # Exécute l'application en utilisant Uvicorn avec les paramètres spécifiés
    uvicorn.run("app:app", host="0.0.0.0", port=8000, log_level="debug")
