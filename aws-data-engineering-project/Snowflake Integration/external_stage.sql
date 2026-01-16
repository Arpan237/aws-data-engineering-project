create or replace stage processed_s3_stage
url = 's3://ecommerce-data-lake/processed/'
storage_integration = s3_int;
