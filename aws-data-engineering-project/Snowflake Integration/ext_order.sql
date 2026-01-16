create or replace external table ext_orders (
    order_id number,
    customer_id number,
    order_amount number,
    order_status string,
    created_at timestamp_ntz,
    order_date date
)
partition by (order_date)
location = @processed_s3_stage/orders/
file_format = (type = parquet);
