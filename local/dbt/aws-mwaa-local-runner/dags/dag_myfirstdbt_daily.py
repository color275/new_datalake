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

default_args = {
    'owner': 'airflow',
    'depends_on_past': True,  # 이전 날짜의 동일한 태스크가 완료되어야 실행
    'retries': 1,
}

# 일반 DAG 생성
with DAG(
    dag_id="myfirstdbt_daily3",
    default_args=default_args,
    schedule_interval="42 0 * * *",
    start_date=datetime(2024, 8, 20, tzinfo=local_tz),
    catchup=True,
    max_active_runs=1,
    concurrency=1,
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
            dbt_vars={"start_date": '{{ ds_nodash }}'},
        ),
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=RenderConfig(
            select=["tag:daily"]
        ),
    )

    # 태스크 의존성 설정
    start >> dbt_task_group >> end
