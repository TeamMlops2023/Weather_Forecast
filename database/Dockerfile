# Utilisez une image de base MySQL 5.7
FROM mysql:5.7

# Définissez les variables d'environnement pour la base de données
ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=mlops_weather
ENV MYSQL_USER=mlops
ENV MYSQL_PASSWORD=mlops

# Installez mysql-connector-python
RUN apt-get update && apt-get install -y python-pip && apt-get clean && pip install mysql-connector-python

# Copiez les fichiers de test dans le conteneur
COPY ./tests /tests

# Exposez le port MySQL (si nécessaire)
EXPOSE 3306
