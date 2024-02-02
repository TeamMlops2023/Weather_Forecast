from airflow import DAG
from airflow.providers.celery.operators.celery import CeleryOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

dag = DAG(
    'ml_model_execution',
    default_args=default_args,
    description='Un DAG pour exécuter un modèle ML dans un pod Kubernetes',
    schedule_interval=None,
)

# Utilisez CeleryOperator ou un opérateur adapté pour votre cas d'utilisation
run_ml_model = CeleryOperator(
    task_id='run_ml_model',
    python_callable=<callable>,
    op_kwargs={'key': 'value'},  # Remplacez par les arguments nécessaires
    dag=dag,
)
