import os
from datetime import datetime

from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping

airflow_home = os.environ["AIRFLOW_HOME"]

profile_config = ProfileConfig(
    profile_name="default",
    target_name="dev",
    profile_mapping=SnowflakeUserPasswordProfileMapping(
        conn_id="snowflake_conn",
        profile_args={"database": "dbt_db", "schema": "dbt_schema"}
    )
)

dbt_snowflake_dag = DbtDag(
    project_config = ProjectConfig("/usr/local/airflow/dags/dbt/",),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(dbt_executable_path=f"{airflow_home}/dbt_venv/bin/dbt",),
    schedule_interval="@daily",
    start_date=datetime(2024, 12, 22),
    catchup=False,
    dag_id="dbt_dag"
)
