# Utilisez l'image de base Python officielle
FROM python:3.8

# Définissez le répertoire de travail dans le conteneur
WORKDIR /usr/src/app

# Copiez les fichiers nécessaires dans le conteneur
COPY src/ .
COPY data/ data/

# Installez les dépendances
RUN pip install numpy==1.26.2
RUN pip install --no-cache-dir -r requirements.txt

# Exposez le port sur lequel l'application va s'exécuter
EXPOSE 8000

# Commande pour démarrer l'application en utilisant uvicorn
CMD ["python", "/usr/src/app/start_server.py"]
