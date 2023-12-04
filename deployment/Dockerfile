# Utiliser l'image de base Python 3.9 slim
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt et les dossiers src et data dans le répertoire de travail du conteneur
COPY requirements.txt src/ data/ /app/

# Installer les dépendances spécifiées dans requirements.txt et nettoyer les caches
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Définir la commande pour démarrer l'application via Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
