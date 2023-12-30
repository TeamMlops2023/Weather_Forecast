# Utilisez une image de base Python
FROM python:3.8-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez les fichiers nécessaires dans le conteneur
COPY . /app

# Installez les dépendances requises
RUN pip install --no-cache-dir -r requirements.txt

# Exposez le port sur lequel FastAPI s'exécutera
EXPOSE 8000

# Commande pour exécuter l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
