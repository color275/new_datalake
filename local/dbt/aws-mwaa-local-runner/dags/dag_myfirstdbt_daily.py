import os
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, RenderConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
import pendulum
from datetime import datetime

# 로컬 타임존 생성
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

# 일반 DAG 생성
with DAG(
    dag_id="myfirstdbt_daily",
    schedule_interval="30 12 * * *",
    start_date=datetime(2024, 8, 9, tzinfo=local_tz),
    catchup=False,
    default_args={"retries": 0},
    user_defined_macros={'local_dt': lambda execution_date: execution_date.in_timezone(
        local_tz).strftime("%Y-%m-%d %H:%M:%S")},
) as dag:

    # 완료 여부를 확인할 DummyOperator 태스크 추가
    start = DummyOperator(task_id='start')
    end = DummyOperator(task_id='end')

    # DbtTaskGroup 생성
    dbt_task_group = DbtTaskGroup(
        group_id="dbt_tasks",
        project_config=ProjectConfig(
            dbt_project_path="/usr/local/airflow/dags/dbt/myfirstdbt",
        ),
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=RenderConfig(
            select=["tag:daily"]
        ),
    )

    # 태스크 의존성 설정
    start >> dbt_task_group >> end
