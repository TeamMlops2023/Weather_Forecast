# Utiliser l'image de base Python 3.9 slim
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier des exigences et le dossier 'src' dans le conteneur
COPY ./requirements.txt /app/
COPY ../src /app/

# Installer les dépendances spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier les autres dossiers nécessaires dans le conteneur
COPY ../data /app/data
COPY ../monitoring/prometheus.yml /app/monitoring/

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Définir la commande pour démarrer l'application via Uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
