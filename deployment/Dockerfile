# creation du docker
FROM python:3.9-slim

WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers nécessaires dans le conteneur
COPY src/ .
COPY data/ ./data/

# Exposer le port sur lequel l'application FastAPI s'exécute
EXPOSE 8000

# Utiliser le script start_server.py pour lancer l'application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
