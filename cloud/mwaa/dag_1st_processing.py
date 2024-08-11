from os import path
from datetime import timedelta  
import airflow  
from airflow import DAG  
import pendulum
from datetime import datetime

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

## 로컬 타임존 생성
local_tz = pendulum.timezone("Asia/Seoul")

dag_name = 'accesslog_parser'
  
default_args = {  
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 10, tzinfo=local_tz),
    'retries': 0,
    'retry_delay': timedelta(minutes=2),
    'provide_context': True,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    dag_name,                         
    default_args=default_args,        
    dagrun_timeout=timedelta(hours=2),
    schedule_interval='*/5 * * * *',  
    catchup=False,
    user_defined_macros={'local_dt': lambda execution_date: execution_date.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
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
                    'accesslog_parser',
                    '--py-files',
                    '/home/hadoop/last_batch_time.py',
                    '/home/hadoop/1st_processing.py',]
      }
  }
]

step1 = EmrAddStepsOperator(
    task_id='accesslog_parser',
    job_flow_id=EMR_CLUSTER_ID,
    aws_conn_id='aws_default',
    steps=SPARK_STEPS,
    dag=dag
)

step1_checker = EmrStepSensor(
    task_id='check_status',
    job_flow_id=EMR_CLUSTER_ID,
    step_id="{{ task_instance.xcom_pull('accesslog_parser', key='return_value')[1] }}",
    aws_conn_id='aws_default',
    dag=dag
)

step1 >> step1_checker



