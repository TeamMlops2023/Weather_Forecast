# Utilisez l'image officielle d'Airflow comme base
FROM apache/airflow:2.2.3

# Copiez vos DAGs dans l'image
COPY ./dags /opt/airflow/dags

# Assurez-vous que les permissions sont correctes
USER root
RUN chown -R airflow: /opt/airflow/dags
USER airflow
