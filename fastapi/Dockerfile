# Utilisez une image de base appropriée pour Python
FROM python:3.8-slim

# Créez un répertoire de travail
WORKDIR /app

# Copiez le code de l'application dans le répertoire de travail
COPY . /app

# Installez les dépendances Python
RUN pip install -r requirements.txt

# Exposez le port sur lequel FastAPI s'exécute
EXPOSE 8000

# Commande pour lancer FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
