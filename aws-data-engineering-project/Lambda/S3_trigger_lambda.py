import json
import boto3
import logging

# ===============================
# Config
# ===============================
GLUE_JOB_NAME = "ecommerce-glue-job"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:xxxx:data-pipeline-alerts"

glue = boto3.client("glue")
sns = boto3.client("sns")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

# ===============================
# Lambda Handler
# ===============================
def lambda_handler(event, context):
    try:
        logger.info(f"Received event: {json.dumps(event)}")

        # Collect all object keys in this event
        s3_objects = [
            (record["s3"]["bucket"]["name"], record["s3"]["object"]["key"])
            for record in event["Records"]
        ]

        # For simplicity, trigger one Glue job per event
        # Pass raw path as Glue argument (dynamic)
        raw_s3_path = f"s3://{s3_objects[0][0]}/{s3_objects[0][1].rsplit('/', 1)[0]}/"
        curated_s3_path = "s3://ecommerce-data-lake/curated/products/"

        response = glue.start_job_run(
            JobName=GLUE_JOB_NAME,
            Arguments={
                "--S3_RAW_PATH": raw_s3_path,
                "--S3_CURATED_PATH": curated_s3_path
            }
        )

        logger.info(f"Started Glue job: {response['JobRunId']} for {raw_s3_path}")

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Pipeline Triggered",
            Message=f"Glue job {GLUE_JOB_NAME} triggered successfully for {raw_s3_path}. JobRunId: {response['JobRunId']}"
        )

    except Exception as e:
        logger.error(f"Pipeline failure: {e}")
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Pipeline Failure",
            Message=f"Pipeline failed: {e}"
        )
        raise
