from airflow import DAG
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.snowflake.operators.snowflake import SnowflakeOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=10),
}

with DAG(
    dag_id="ecommerce_data_pipeline",
    default_args=default_args,
    description="End-to-end pipeline: API → S3 → Glue → Snowflake → dbt",
    schedule_interval="@daily",
    start_date=datetime(2026, 1, 10),
    catchup=False,
    tags=["ecommerce", "aws", "snowflake", "dbt"],
) as dag:

    # API Ingestion (optional if Lambda handles it)
    api_ingestion = BashOperator(
        task_id="api_to_s3",
        bash_command="python /ingestion/api_to_s3.py"
    )

    # Run Glue ETL job
    glue_etl = GlueJobOperator(
        task_id="glue_etl",
        job_name="ecommerce-glue-job",
        script_args={
            "--S3_RAW_PATH": "s3://ecommerce-data-lake/raw/api/products/",
            "--S3_CURATED_PATH": "s3://ecommerce-data-lake/curated/products/"
        },
        region_name="us-east-1"
    )

    # Load into Snowflake (COPY command)
    snowflake_copy_raw = SnowflakeOperator(
        task_id="snowflake_copy_raw",
        snowflake_conn_id="snowflake_default",
        sql="snowflake/copy_into_tables.sql"
    )

    # dbt run
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /dbt && dbt run"
    )

    # dbt test
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /dbt && dbt test"
    )

    # Optional: refresh external tables
    refresh_external = SnowflakeOperator(
        task_id="refresh_snowflake_external",
        snowflake_conn_id="snowflake_default",
        sql="""
        alter external table ext_orders refresh;
        alter external table ext_customers refresh;
        alter external table ext_products refresh;
        """
    )

    # Dependency chain
    api_ingestion >> glue_etl >> snowflake_copy_raw >> dbt_run >> dbt_test >> refresh_external
