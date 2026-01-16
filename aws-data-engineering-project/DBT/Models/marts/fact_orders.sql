{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select
    o.order_id,
    o.customer_id,
    o.product_id,
    o.order_date,
    o.amount
from {{ ref('stg_orders') }} o

{% if is_incremental() %}
where o.order_date > (
    select max(order_date) from {{ this }}
)
{% endif %}
