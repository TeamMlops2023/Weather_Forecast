# Utilisez une image MySQL existante depuis Docker Hub
FROM mysql:5.7
# Définissez les variables d'environnement pour la configuration MySQL
ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=mlops_weather
ENV MYSQL_USER=mlops
ENV MYSQL_PASSWORD=mlops

# Copiez le répertoire 'tests' dans le conteneur
COPY ./tests /tests  

# Exposez le port MySQL (par défaut : 3306)
EXPOSE 3306
