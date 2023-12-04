# Utiliser l'image de base Python 3.9 slim
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le répertoire de travail du conteneur
COPY ./requirements.txt .

# Installer les dépendances spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers des dossiers src et data dans le conteneur
COPY ./src/ ./src/
COPY ./data/* ./data/

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Définir la commande pour démarrer l'application via Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

