FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=mlops_weather
ENV MYSQL_USER=mlops
ENV MYSQL_PASSWORD=mlops

# Installez pip
RUN apt-get update && \
    apt-get install -y python-pip && \
    apt-get clean

# Installez le module mysql-connector-python
RUN pip install mysql-connector-python

COPY ./tests /tests

EXPOSE 3306


