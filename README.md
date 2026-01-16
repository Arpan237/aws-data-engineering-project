# aws-data-engineering-project

## 📂 Dataset

This project uses a synthetic e-commerce dataset created for learning and demonstration purposes.

### Files
- orders.csv – transactional order data
- customers.json – customer master data
- products.csv – product catalog


# Overview

This project demonstrates a production-grade, cloud-native data engineering platform designed using modern industry tools and best practices.
It supports batch processing, API ingestion, and event-driven pipelines, similar to real-world enterprise data platforms.

The project is built entirely using personal/free-tier compatible cloud services, making it realistic, truthful, and interview-safe.

# Business Use Case

An E-commerce Analytics Platform that enables:

Sales and revenue reporting

Customer behavior analysis

Product performance insights

Near real-time ingestion of new data files

# High-Level Architecture

## Data Ingestion Patterns
## Batch Ingestion (Scheduled)

CSV files uploaded to S3

Triggered daily using Apache Airflow

## API-Based Ingestion

Public REST API data fetched using Python

Stored as raw JSON in S3

## Event-Driven Ingestion

S3 object arrival triggers AWS Lambda

Lambda triggers AWS Glue ETL job

## Technology Stack

Source	: CSV Files, Public REST API,JSON
Storage	: Amazon S3
Event   : Trigger	AWS Lambda
ETL Processing	: AWS Glue (PySpark)
Orchestration	: Apache Airflow
Alerting	: Amazon SNS
Failure Handling	: SQS Dead Letter Queue
Warehouse	: Snowflake
Transformations : dbt
Data Format	: Parquet

## Repository Structure
aws-data-engineering-project/
│
├── airflow/
│   └── dags/
│       └── ecommerce_pipeline_dag.py
│
├── glue/
│   └── ecommerce_glue_job.py
│
├── lambda/
│   └── s3_trigger_lambda.py
│
├── ingestion/
│   └── api_ingestion.py
│
├── snowflake/
│   ├── create_tables.sql
│   └── stage_and_copy.sql
│
├── dbt/
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/
│       ├── marts/
│       │   ├── dim_customers.sql
│       │   └── fct_orders.sql
│
├── datasets/
│   ├── customers.csv
│   └── orders.csv
│
├── diagrams/
│   └── architecture.png
│
└── README.md

## End-to-End Pipeline Execution Flow
🔹 Step 1: Data Ingestion

CSV files uploaded to S3 (raw/ bucket)

API data fetched via Python script and stored in S3

🔹 Step 2: Event Trigger

S3 upload triggers AWS Lambda

Lambda starts AWS Glue ETL job

🔹 Step 3: ETL Processing (Glue)

Reads raw data from S3

Applies schema enforcement and cleansing

Writes transformed data to S3 in Parquet format

🔹 Step 4: Orchestration (Airflow)

Airflow DAG:

Triggers Glue job (batch mode)

Loads data into Snowflake

Runs dbt transformations

🔹 Step 5: Data Warehousing (Snowflake)

External stage reads data from S3

COPY command loads data into raw tables

🔹 Step 6: Analytics Engineering (dbt)

Staging models clean raw data

Fact & dimension models created

Incremental loading implemented

SCD Type-2 applied for customer dimension

🔹 Step 7: Monitoring & Alerts

Success and failure notifications via SNS

Lambda failures routed to SQS DLQ
