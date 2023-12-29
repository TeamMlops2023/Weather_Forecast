# Utilisation d'une image Python officielle
FROM python:3.8-slim

# Définition du répertoire de travail
WORKDIR /app

# Copie du fichier des dépendances et installation
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source du modèle ML
COPY modele.py .

# Exposition du port (si votre modèle ML utilise un serveur web/Flask)
EXPOSE 5000

# Commande pour lancer le service ML
CMD ["python", "modele.py"]
