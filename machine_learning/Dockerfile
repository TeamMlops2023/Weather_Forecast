# Utilisez l'image Python 3.8 slim comme base
FROM python:3.8-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier de dépendances et installez les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le script Python du modèle et les données nécessaires
COPY modele.py .
COPY data/ data/

# Définissez la commande pour exécuter le service Flask
CMD ["python", "modele.py"]
