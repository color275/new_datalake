import os
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.constants import ExecutionMode
import pendulum
from datetime import datetime, timedelta

## 로컬 타임존 생성
local_tz = pendulum.timezone("Asia/Seoul")

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgresql_dbt",
        profile_args={"schema": "stg"},
    )
)

execution_config = ExecutionConfig(
    dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt",
)

def prev_execution_dt(dt, **kwargs):
    return dt - timedelta(minutes=1)

# 일반 DAG 생성
with DAG(
    dag_id="myfirstdbt_hourly",
    schedule_interval="30 12 * * *",
    start_date=datetime(2024, 8, 9, tzinfo=local_tz),
    catchup=False,
    default_args={"retries": 0},
    user_defined_macros={'local_dt': lambda execution_date: execution_date.in_timezone(local_tz).strftime("%Y-%m-%d %H:%M:%S")},
) as dag:

    # ExternalTaskSensor 생성
    wait_for_daily = ExternalTaskSensor(
        task_id='wait_for_daily',
        external_dag_id='myfirstdbt_daily',
        external_task_id='end',
        allowed_states=['success'],
        # execution_delta=timedelta(minutes=1),
        execution_date_fn=prev_execution_dt,
        mode='poke',
        dag=dag,
    )
    
    # DbtTaskGroup 생성
    dbt_task_group = DbtTaskGroup(
        group_id="dbt_tasks",
        project_config=ProjectConfig(
            dbt_project_path="/usr/local/airflow/dags/dbt/myfirstdbt",
        ),
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=RenderConfig(
            select=["tag:hourly"]
        ),
    )

    # 태스크 의존성 설정
    wait_for_daily >> dbt_task_group