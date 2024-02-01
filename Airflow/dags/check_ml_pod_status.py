from kubernetes import client, config
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

def check_ml_pod_status():
    config.load_kube_config()  # Utiliser load_incluster_config() si exécuté à l'intérieur d'un cluster Kubernetes
    v1 = client.CoreV1Api()
    # Remplacez "ml-model-deployment-abc123" par le nom réel de votre pod de modèle ML
    pod_status = v1.read_namespaced_pod_status(name="ml-model-deployment-7ccc6bb9f7-2klcl", namespace="test")
    print(f"Pod Status: {pod_status.status.phase}")
    # Ajoutez ici la logique pour réagir en fonction de l'état du pod

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2021, 1, 1),
    'retries': 1,
}

dag = DAG('check_ml_pod_status_dag', default_args=default_args, schedule_interval='@daily')

t1 = PythonOperator(
    task_id='check_ml_pod_status_task',
    python_callable=check_ml_pod_status,
    dag=dag,
)

t1
