import json
import boto3

glue = boto3.client("glue")
sns = boto3.client("sns")

GLUE_JOB_NAME = "ecommerce-glue-job"
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:xxxx:data-pipeline-alerts"

def lambda_handler(event, context):
    try:
        for record in event["Records"]:
            bucket = record["s3"]["bucket"]["name"]
            key = record["s3"]["object"]["key"]

            glue.start_job_run(JobName=GLUE_JOB_NAME)

        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Pipeline Triggered",
            Message="Glue job triggered successfully from S3 event."
        )

    except Exception as e:
        sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject="Pipeline Failure",
            Message=str(e)
        )
        raise
