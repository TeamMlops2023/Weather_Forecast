# Utilisez l'image MySQL officielle comme base
FROM mysql:5.7

# Définissez les variables d'environnement pour la configuration de MySQL
ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=mlops_weather
ENV MYSQL_USER=mlops
ENV MYSQL_PASSWORD=mlops

# Copiez les scripts de test dans l'image
COPY ./tests /tests

# Installez Python et le connecteur MySQL pour Python
RUN apt-get update && \
    apt-get install -y python-pip && \
    pip install mysql-connector-python

# Exposez le port pour MySQL
EXPOSE 3306

