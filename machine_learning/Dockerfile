# Utilisez une image Python officielle
FROM python:3.8-slim

# Définissez le répertoire de travail
WORKDIR /app

# Copiez les fichiers de dépendances et installez-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le code source de votre modèle
COPY modele.py .

# Commande pour lancer le service ML
CMD ["python", "modele.py"]
