from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, to_timestamp, lower

# =================================================
# Spark Session
# =================================================
spark = (
    SparkSession.builder
    .appName("EcommerceGlueJob")
    .getOrCreate()
)

# =================================================
# S3 Buckets
# =================================================
RAW_BUCKET = "s3://ecommerce-data-lake/raw"
PROCESSED_BUCKET = "s3://ecommerce-data-lake/processed"

# =================================================
# ORDERS | CSV → PARQUET
# =================================================
orders_df = (
    spark.read
    .option("header", "true")
    .csv(f"{RAW_BUCKET}/orders/")
)

orders_clean_df = (
    orders_df
    .dropDuplicates(["order_id"])
    .select(
        col("order_id").cast("int").alias("order_id"),
        col("customer_id").cast("int").alias("customer_id"),
        to_date(col("order_date")).alias("order_date"),
        col("amount").cast("double").alias("order_amount"),
        col("status").cast("string").alias("order_status"),
        to_timestamp(col("created_at")).alias("created_at")
    )
    .filter(col("order_id").isNotNull())
)

orders_clean_df.write \
    .mode("overwrite") \
    .parquet(f"{PROCESSED_BUCKET}/orders/")

# =================================================
# CUSTOMERS | JSON → PARQUET + CSV
# =================================================
customers_df = (
    spark.read
    .option("multiline", "true")
    .json(f"{RAW_BUCKET}/customers/")
)

customers_clean_df = (
    customers_df
    .dropDuplicates(["customer_id"])
    .select(
        col("customer_id").cast("int").alias("customer_id"),
        col("first_name").cast("string").alias("first_name"),
        col("last_name").cast("string").alias("last_name"),
        lower(col("email")).cast("string").alias("email"),
        to_timestamp(col("created_at")).alias("created_at")
    )
    .filter(col("customer_id").isNotNull())
)

# Parquet (analytics / dbt)
customers_clean_df.write \
    .mode("overwrite") \
    .parquet(f"{PROCESSED_BUCKET}/customers/parquet/")

# CSV (Snowflake COPY)
customers_clean_df.write \
    .mode("overwrite") \
    .option("header", "true") \
    .csv(f"{PROCESSED_BUCKET}/customers/csv/")

# =================================================
# PRODUCTS | API JSON → PARQUET
# =================================================
products_df = (
    spark.read
    .option("multiline", "true")
    .json(f"{RAW_BUCKET}/api/products/")
)

products_clean_df = (
    products_df
    .select(
        col("id").cast("int").alias("product_id"),
        col("title").cast("string").alias("product_name"),
        col("category").cast("string").alias("category"),
        col("price").cast("double").alias("price"),
        to_timestamp(col("created_at")).alias("created_at")
    )
    .dropDuplicates(["product_id"])
    .filter(col("product_id").isNotNull())
)

products_clean_df.write \
    .mode("overwrite") \
    .parquet(f"{PROCESSED_BUCKET}/products/")

print("==============================================")
print(" Ecommerce Glue Job Completed Successfully ")
print(" Raw → Processed (Parquet + CSV) ")
print("==============================================")
