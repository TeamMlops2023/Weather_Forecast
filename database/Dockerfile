FROM mysql:5.7

ENV MYSQL_ROOT_PASSWORD=mysecretpassword
ENV MYSQL_DATABASE=mlops_weather
ENV MYSQL_USER=mlops
ENV MYSQL_PASSWORD=mlops

RUN pip install mysql-connector-python

COPY ./tests /tests

EXPOSE 3306


