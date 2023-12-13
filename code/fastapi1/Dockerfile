# Utiliser l'image de base Python 3.9 slim
# FROM python:3.9-slim
FROM python:3.8.10-slim

# Mise à jour et installation des bibliothèques nécessaires
# Met à jour la liste des paquets disponibles pour l'installation
# Installe le paquet python3-pip
# Met à jour le gestionnaire de paquets Python (pip) 
# Nettoie le cache des paquets téléchargés par apt-get pour réduire la taille de l'image Docker.
# Supprime le contenu du répertoire /var/lib/apt/lists/, qui contient les listes de paquets téléchargés. Cela est également fait pour réduire la taille de l'image Docker.

RUN apt-get update && \
    apt-get install -y python3-pip && \
    python3 -m pip install --upgrade pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r /app/src/requirements.txt

# Exposer le port 8000 pour l'application FastAPI
EXPOSE 8000

# Définir la commande pour démarrer l'application via start_server.py
CMD ["python", "src/start_server.py"]
