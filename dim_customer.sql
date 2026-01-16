{{ config(
    materialized='incremental',
    unique_key='customer_id'
) }}

with source as (
    select
        customer_id,
        customer_name,
        city,
        current_timestamp as valid_from
    from {{ ref('stg_customers') }}
),

final as (
    select
        s.customer_id,
        s.customer_name,
        s.city,
        s.valid_from,
        null as valid_to,
        true as is_current
    from source s
)

select * from final
