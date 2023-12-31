FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=mlops_weather
ENV MYSQL_USER=mlops
ENV MYSQL_PASSWORD=mlops

COPY ./tests /tests

# Installez Python et le connecteur MySQL en utilisant les commandes disponibles dans l'image
RUN apt-get update && \
    apt-get install -y python && \
    apt-get install -y python-pip && \
    pip install mysql-connector-python

EXPOSE 3306


