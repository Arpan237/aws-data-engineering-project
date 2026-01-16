# aws-data-engineering-project

## 📂 Dataset

This project uses a synthetic e-commerce dataset created for learning and demonstration purposes.

### Files
- orders.csv – transactional order data
- customers.json – customer master data
- products.csv – product catalog



## 📌 Overview

This project demonstrates a **production-style, cloud-native data engineering platform** designed using modern industry tools and best practices.

The pipeline supports **batch ingestion, API-based ingestion, and event-driven processing**, similar to real-world enterprise data platforms used for analytics and reporting.

All components are built using **personal cloud accounts and free-tier compatible services**, making this project fully reproducible, ethical, and interview-safe.

---

## 🧠 Business Use Case

An **E-commerce Analytics Platform** that enables:

- Sales and revenue analysis  
- Customer behavior tracking  
- Product performance reporting  
- Near real-time ingestion of newly arrived data  

---

## 🏗️ High-Level Architecture

![Architecture Diagram](diagrams/architecture_diagram.png,pipeline.png)

---

## 🔄 Data Ingestion Patterns

### 1️⃣ Batch Ingestion
- CSV files uploaded to Amazon S3
- Orchestrated using **Apache Airflow**

### 2️⃣ API-Based Ingestion
- Public REST API data ingested using Python
- Stored in Amazon S3 as raw JSON

### 3️⃣ Event-Driven Ingestion
- S3 object upload triggers **AWS Lambda**
- Lambda automatically starts **AWS Glue ETL jobs**

---

## 🧰 Technology Stack

| Layer | Technology |
|-----|-----------|
Data Sources | CSV Files, Public REST APIs |
Storage | Amazon S3 |
Event Trigger | AWS Lambda |
ETL Processing | AWS Glue (PySpark) |
Orchestration | Apache Airflow |
Alerting | Amazon SNS |
Failure Handling | Amazon SQS (DLQ) |
Warehouse | Snowflake |
Transformations | dbt |
Data Format | Parquet |

---

## 📂 Repository Structure

```text
aws-data-engineering-project/
│
├── ingestion/
│   └── API_to_s3.py
│
├── lambda/
│   └── S3_trigger_lambda.py
│
├── glue/
│   └── ecommerce_glue_job.py
│
├── airflow/
│   └── dags/
│       └── ecommerce_pipeline_dag.py
│
├── snowflake/
│   ├── create_tables.sql
│   └── stage_and_copy.sql
│
├── dbt/
│   ├── dbt_project.yml
│   └── models/
│       ├── staging/
│       │   ├── stg_orders.sql
│       │   └── stg_customers.sql
│       └── marts/
│           ├── fact_orders.sql
│           └── dim_customers.sql
│
├── datasets/
│   ├── customers.csv
│   ├── orders.csv
│   └── products.csv
│
├── diagrams/
│   └── architecture_diagram.png
|   |__ pipeline.png
│
├── SNS.md
├── DLQ_flow.md
└── README.md
