import os
from datetime import datetime
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping
from cosmos.constants import ExecutionMode
import pendulum

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

my_cosmos_dag = DbtDag(
    project_config=ProjectConfig(
        dbt_project_path="/usr/local/airflow/dags/dbt/myfirstdbt",
    ),
    profile_config=profile_config,
    execution_config=execution_config,
    # normal dag parameters
    schedule_interval="@hourly",
    start_date=datetime(2024, 8, 9, tzinfo=local_tz),
    catchup=False,
    dag_id="myfirstdbt",
    default_args={"retries": 0},
)
