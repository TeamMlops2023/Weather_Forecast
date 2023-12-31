# Utilisez une image de base Ubuntu
FROM ubuntu:20.04

# Mise à jour du système et installation de MySQL
RUN apt-get update && apt-get install -y mysql-server mysql-client && apt-get clean

# Configuration de l'utilisateur et du mot de passe MySQL
ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=mlops_weather
ENV MYSQL_USER=mlops
ENV MYSQL_PASSWORD=mlops

# Installez mysql-connector-python
RUN apt-get install -y python3-pip && pip3 install mysql-connector-python

# Exposez le port MySQL (si nécessaire)
EXPOSE 3306

# Commande pour démarrer MySQL
CMD ["mysqld"]
