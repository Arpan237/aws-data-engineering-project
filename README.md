# AWS Data Engineering Project

## Overview

This repository showcases an **end-to-end AWS-based data engineering pipeline** designed using modern, industry-standard tools. The project simulates how raw data is ingested, processed, transformed, and modeled into analytics-ready datasets for downstream reporting and analysis.

The focus of this project is **clarity of architecture, modular design, and production-oriented thinking**, rather than just writing scripts.

---

## Architecture

![Architecture Diagram](aws-data-engineering-project
/Architecture_diagram/architecture_diagram.png)

---

## End-to-End Data Flow

1. Data is ingested from an external source using a Python-based ingestion script
2. Raw data is stored in **Amazon S3**
3. **S3 events trigger AWS Lambda** for orchestration
4. **AWS Glue** performs ETL processing and transformations
5. Transformed data is loaded into **Snowflake** using staging and COPY commands
6. **dbt** builds staging and mart-level models for analytics
7. **Apache Airflow** orchestrates and schedules the pipeline
8. **SNS and DLQ** handle alerts and failure scenarios

---

## Tech Stack

* **Cloud Platform:** AWS (S3, Lambda, Glue, SNS)
* **Orchestration:** Apache Airflow
* **Data Warehouse:** Snowflake
* **Transformation Layer:** dbt
* **Languages:** Python, SQL
* **Version Control:** Git, GitHub
* **CI/CD:** GitHub Actions

---

## Project Structure

```
aws-data-engineering-project/
├── ingestion/            # API ingestion scripts
├── lambda/               # AWS Lambda functions
├── glue/                 # AWS Glue ETL jobs
├── airflow/dags/         # Airflow DAGs
├── snowflake/            # Snowflake DDL & COPY scripts
├── dbt/                  # dbt project and models
│   ├── models/
│   │   ├── staging/      # Source-aligned models
│   │   └── marts/        # Business-level models
├── datasets/             # Sample datasets
├── diagrams/             # Architecture diagrams
├── SNS.md                # Notification flow
├── DLQ_flow.md           # Failure handling design
└── README.md
```

---

## dbt Modeling Approach

### Staging Layer

* One-to-one mapping with source tables
* Light transformations only (casting, renaming, filtering)
* Naming convention: `stg_<source>_<entity>`

### Mart Layer

* Business-ready fact and dimension tables
* Optimized for analytics and reporting
* Naming convention:

  * Facts: `fact_<business_process>`
  * Dimensions: `dim_<entity>`

---

## Data Quality & Testing

The project includes **dbt tests** to ensure:

* Primary keys are unique
* Mandatory fields are not null
* Referential integrity between fact and dimension tables

---

## CI/CD

A lightweight **GitHub Actions CI pipeline** validates:

* Python syntax
* Repository structure
* SQL/dbt model presence

This ensures consistent quality without executing cloud resources.

---

## Future Enhancements

* dbt snapshots and incremental models
* Data quality checks with dbt-expectations
* Terraform for AWS infrastructure
* Cost optimization strategies for Snowflake

---

## Author

**Arpan Hazra**
Data Engineer | AWS | Snowflake | DBT | SQL | Airflow

GitHub: [https://github.com/Arpan237](https://github.com/Arpan237)
