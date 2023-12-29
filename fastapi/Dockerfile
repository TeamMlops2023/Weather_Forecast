# Utilisation d'une image Python officielle
FROM python:3.8-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie du fichier des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'application FastAPI
COPY main.py .

# Exposition du port (assurez-vous que cela correspond au port utilisé par Uvicorn)
EXPOSE 8000

# Commande pour lancer l'application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
