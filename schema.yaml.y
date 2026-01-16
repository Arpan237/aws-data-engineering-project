version: 2

models:
  - name: fact_orders
    tests:
      - not_null:
          column_name: order_id
      - unique:
          column_name: order_id
