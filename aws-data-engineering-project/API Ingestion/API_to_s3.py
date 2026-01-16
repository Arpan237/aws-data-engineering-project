import os
import json
import boto3
import requests
import logging
from datetime import datetime
from time import sleep

# ===============================
# Configuration (environment-friendly)
# ===============================
S3_BUCKET = os.environ.get("S3_BUCKET", "ecommerce-data-lake")
S3_PREFIX = os.environ.get("S3_PREFIX", "raw/api/products")
API_URL = os.environ.get("API_URL", "https://fakestoreapi.com/products")
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", 3))
RETRY_DELAY = int(os.environ.get("RETRY_DELAY", 5))  # seconds

# ===============================
# Logging setup
# ===============================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# ===============================
# AWS S3 client
# ===============================
s3 = boto3.client("s3")


# ===============================
# Functions
# ===============================
def fetch_api_data(url: str) -> list:
    """
    Fetch data from API with basic retry logic.
    Returns a list of records.
    """
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            if not isinstance(data, list):
                raise ValueError("API did not return a list of records")
            logger.info(f"Successfully fetched {len(data)} records from API")
            return data
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt < MAX_RETRIES:
                sleep(RETRY_DELAY)
            else:
                logger.error("Max retries reached. Exiting.")
                raise


def upload_to_s3(data: list, bucket: str, prefix: str):
    """
    Upload JSON data to S3 with a timestamped filename.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"products_{timestamp}.json"
    s3_key = f"{prefix}/{file_name}"

    try:
        s3.put_object(Bucket=bucket, Key=s3_key, Body=json.dumps(data, indent=2))
        logger.info(f"Uploaded data to S3: s3://{bucket}/{s3_key}")
    except Exception as e:
        logger.error(f"Failed to upload to S3: {e}")
        raise


# ===============================
# Main execution
# ===============================
def main():
    logger.info("Starting API → S3 pipeline")
    data = fetch_api_data(API_URL)
    upload_to_s3(data, S3_BUCKET, S3_PREFIX)
    logger.info("Pipeline completed successfully")


if __name__ == "__main__":
    main()
