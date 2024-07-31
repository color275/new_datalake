from os import path
from datetime import timedelta  
import airflow  
from airflow import DAG  

from airflow.providers.amazon.aws.operators.emr import (
    EmrAddStepsOperator,
    EmrCreateJobFlowOperator,
    EmrTerminateJobFlowOperator,
)
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.glue_crawler import GlueCrawlerOperator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator

dag_name = 'orders_iceberg_cdc_from_kafka'
  
default_args = {  
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
    'provide_context': True,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    dag_name,                         # dag_name은 변수로, DAG의 이름을 지정합니다.
    default_args=default_args,        # default_args는 기본 설정들을 포함한 딕셔너리입니다.
    dagrun_timeout=timedelta(hours=2),# DAG 실행 최대 시간을 2시간으로 설정
    schedule_interval='*/5 * * * *',  # 5분마다 실행되도록 cron 표현식 설정
    catchup=False
)

S3_URI = "s3://ken-datalake/emr/src/"
EMR_CLUSTER_ID = 'j-8G0P9GVGUYGM'

SPARK_STEPS = [
  {
      'Name': 'setup - copy files',
      'ActionOnFailure': 'CANCEL_AND_WAIT',
      'HadoopJarStep': {
          'Jar': 'command-runner.jar',
          'Args': ['aws', 's3', 'cp', '--recursive', S3_URI, '/home/hadoop/']
      }
  },
  {
      'Name': 'Run Spark',
      'ActionOnFailure': 'CANCEL_AND_WAIT',
      'HadoopJarStep': {
          'Jar': 'command-runner.jar',
          'Args': [ 'spark-submit',
                    '--master',
                    'yarn',
                    '--deploy-mode',
                    'cluster',
                    '--name',
                    'orders_iceberg_cdc',
                    '--py-files',
                    '/home/hadoop/last_batch_time.py',
                    '/home/hadoop/orders_iceberg_cdc.py',]
      }
  }
]

step1 = EmrAddStepsOperator(
    task_id='add_steps',
    job_flow_id=EMR_CLUSTER_ID,
    aws_conn_id='aws_default',
    steps=SPARK_STEPS,
    dag=dag
)

step1_checker = EmrStepSensor(
    task_id='watch_step1',
    job_flow_id=EMR_CLUSTER_ID,
    step_id="{{ task_instance.xcom_pull('add_steps', key='return_value')[1] }}",
    aws_conn_id='aws_default',
    dag=dag
)

step1 >> step1_checker



