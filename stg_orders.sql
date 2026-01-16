select
  order_id,
  customer_id,
  product_id,
  order_date,
  amount
from raw.orders
where amount > 0