from airflow import DAG
from airflow.providers.celery.operators.celery import CeleryOperator
from airflow.providers.celery.operators.celery import KubernetesPodOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
}

with DAG(
    'ml_model_execution',
    default_args=default_args,
    description='A DAG to execute an ML model task',
    schedule_interval=None,
) as dag:

    task1 = KubernetesPodOperator(
        namespace='test',
        image='mlopsweather2023/ml-model-image:latest',
        cmds=["python", "modele.py"],
        name="ml-model-task",
        task_id="run_ml_model",
        is_delete_operator_pod=False,
        in_cluster=True,
        get_logs=True,
    )
