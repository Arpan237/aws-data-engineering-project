from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.amazon.aws.operators.glue import AwsGlueJobOperator
from datetime import datetime

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 1, 13),
    "email": ["your_email@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1
}

with DAG(
    dag_id="ecommerce_end_to_end_pipeline",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False
) as dag:

    api_ingestion = BashOperator(
        task_id="api_to_s3",
        bash_command="python /ingestion/api_to_s3.py"
    )

    glue_etl = AwsGlueJobOperator(
        task_id="glue_etl",
        job_name="ecommerce-glue-job",
        region_name="us-east-1"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /dbt && dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /dbt && dbt test"
    )

    api_ingestion >> glue_etl >> dbt_run >> dbt_test
