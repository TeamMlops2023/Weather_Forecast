# Utilisez l'image officielle d'Airflow avec un tag spécifique comme base
FROM apache/airflow:2.2.3

# (Optionnel) Installez des dépendances supplémentaires ou des outils, par exemple `kubectl`
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiez vos DAGs dans l'image
COPY --chown=airflow:airflow ./dags /opt/airflow/dags

# Changez l'utilisateur en airflow
USER airflow
