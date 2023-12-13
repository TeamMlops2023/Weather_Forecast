# Image de départ
FROM ubuntu:18.04

# Update et installation de library
RUN apt-get update && apt-get install -y python3-pip
RUN pip3 install requests

# Copiez le fichier wait-for-it.sh dans l'image
COPY wait-for-it.sh /my_test/wait-for-it.sh
RUN chmod +x /my_test/wait-for-it.sh

# Ajoute le fichier .py dans le container à tel chemin
ADD src/test_fastapi1.py /my_test/test_fastapi1.py

# Création d'une variable d'environnement
ENV LOG=1

# Exécution de la commande python
# CMD python3 /my_test/test_fastapi1.py