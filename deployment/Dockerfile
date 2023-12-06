# Utiliser l'image de base Python 3.9 slim
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des exigences dans le conteneur
COPY requirements.txt /app/

# Installer les dépendances spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers/dossiers nécessaires dans le conteneur
COPY src/ /app/
COPY data/ /app/data/
COPY monitoring/ /app/monitoring/

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Définir la commande pour démarrer l'application via start_server.py
CMD ["python", "src/start_server.py"]
