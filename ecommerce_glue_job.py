from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

spark = SparkSession.builder.appName("EcommerceGlueJob").getOrCreate()

RAW_BUCKET = "s3://ecommerce-data-lake/raw"
PROCESSED_BUCKET = "s3://ecommerce-data-lake/processed"

# Orders
orders_df = spark.read.option("header", "true").csv(f"{RAW_BUCKET}/orders/")
orders_clean = (
    orders_df
    .dropDuplicates(["order_id"])
    .withColumn("order_date", to_date(col("order_date")))
    .withColumn("amount", col("amount").cast("double"))
)

orders_clean.write.mode("overwrite").parquet(f"{PROCESSED_BUCKET}/orders/")

# Customers
customers_df = spark.read.json(f"{RAW_BUCKET}/customers/")
customers_clean = customers_df.dropDuplicates(["customer_id"])

customers_clean.write.mode("overwrite").parquet(f"{PROCESSED_BUCKET}/customers/")


# API Products
products = spark.read.json(f"{RAW_BUCKET}/api/products/")
products_clean = products.select(
    col("id").alias("product_id"),
    col("title").alias("product_name"),
    col("category"),
    col("price")
)

products_clean.write.mode("overwrite").parquet(f"{PROCESSED_BUCKET}/products/")
