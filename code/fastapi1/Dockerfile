# Utilisez une image Python officielle comme image de base
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copier les fichiers nécessaires dans le conteneur
COPY src/ .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel FastAPI s'exécutera
EXPOSE 8000

# Commande pour lancer l'application FastAPI
CMD ["python", "./start_server.py"]
