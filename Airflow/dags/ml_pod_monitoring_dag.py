from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator
from airflow.operators.dummy import DummyOperator

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

monitor_ml_pod = KubernetesPodOperator(
    namespace='default',
    image='alpine',
    cmds=["sh", "-c", "kubectl get pods -n test | grep ml-model-deployment-7ccc6bb9f7-2694b"],
    name='monitor-ml-pod',
    task_id='monitor_ml_pod_task',
    get_logs=True,
    dag=dag
)

start >> monitor_ml_pod
