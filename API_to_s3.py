import requests
import json
import boto3
from datetime import datetime

S3_BUCKET = "ecommerce-data-lake"
S3_PREFIX = "raw/api/products"

API_URL = "https://fakestoreapi.com/products"

s3 = boto3.client("s3")

def fetch_api_data():
    response = requests.get(API_URL)
    response.raise_for_status()
    return response.json()

def upload_to_s3(data):
    file_name = f"products_{datetime.now().strftime('%Y%m%d')}.json"
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=f"{S3_PREFIX}/{file_name}",
        Body=json.dumps(data)
    )

if __name__ == "__main__":
    data = fetch_api_data()
    upload_to_s3(data)
