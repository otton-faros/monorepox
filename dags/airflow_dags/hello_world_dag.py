from collections import defaultdict

from pathlib import Path

from airflow import DAG
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.version import version
from datetime import datetime, timedelta

from kedro.framework.session import KedroSession
from kedro.framework.project import configure_project


class KedroOperator(BaseOperator):
    @apply_defaults
    def __init__(self, package_name: str, pipeline_name: str, node_name: str, project_path: str, env: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.package_name = package_name
        self.pipeline_name = pipeline_name
        self.node_name = node_name
        self.project_path = project_path
        self.env = env

    def execute(self, context):
        configure_project(self.package_name)
        with KedroSession.create(self.package_name, self.project_path, env=self.env) as session:
            session.run(self.pipeline_name, node_names=[self.node_name])


# Kedro settings required to run your pipeline
env = "local"
pipeline_name = "__default__"
project_path = Path.cwd()
package_name = "hello_world"

# Default settings applied to all tasks
default_args = {"owner": "airflow", "depends_on_past": False, "email_on_failure": False, "email_on_retry": False, "retries": 2, "retry_delay": timedelta(minutes=1)}

# Using a DAG context manager, you don't have to specify the dag property of each task
with DAG(
    "hello-world",
    start_date=datetime(2019, 1, 1),
    max_active_runs=3,
    schedule_interval=timedelta(minutes=1),  # https://airflow.apache.org/docs/stable/scheduler.html#dag-runs
    default_args=default_args,
    catchup=False,  # enable if you don't want historical dag runs to run
) as dag:

    tasks = {}

    tasks["define-greet"] = KedroOperator(
        task_id="define-greet",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="define_greet",
        project_path=project_path,
        env=env,
    )

    tasks["join-with-greet"] = KedroOperator(
        task_id="join-with-greet",
        package_name=package_name,
        pipeline_name=pipeline_name,
        node_name="join_with_greet",
        project_path=project_path,
        env=env,
    )

    tasks["define-greet"] >> tasks["join-with-greet"]
