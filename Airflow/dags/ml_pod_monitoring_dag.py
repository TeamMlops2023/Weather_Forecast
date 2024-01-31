from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator
from kubernetes import client, config

config.load_incluster_config()  # Chargez la configuration Kubernetes à partir de l'environnement du pod

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ml_pod_monitoring',
    default_args=default_args,
    description='A simple DAG to monitor ML pod',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 31),
    catchup=False,
)

start = DummyOperator(task_id='start', dag=dag)

# Utilisez l'API Kubernetes pour obtenir l'état du pod ML
def get_ml_pod_status():
    api = client.CoreV1Api()
    pod_name = "ml-model-deployment-7ccc6bb9f7-4lzsw"  
    pod_namespace = "test"  
    try:
        pod_status = api.read_namespaced_pod_status(name=pod_name, namespace=pod_namespace)
        return pod_status.status.phase
    except Exception as e:
        return str(e)

monitor_ml_pod = PythonOperator(
    task_id='monitor_ml_pod_task',
    python_callable=get_ml_pod_status,
    dag=dag
)

start >> monitor_ml_pod
