{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select
    order_id,
    customer_id,
    order_date,
    order_amount,
    order_status,
    created_at
from {{ ref('stg_orders') }}

{% if is_incremental() %}
where created_at > (select max(created_at) from {{ this }})
{% endif %}
