import json
import boto3
import email
import base64


bucket_name = "sample-email-box"

# Sender Email address
SENDER = "XXXX@XXX.com"
# Recipent Email address
RECIPIENT="XXXX@XXXX.com"


def send_mail(message):
    AWS_REGION = "us-east-1"
    ses_client = boto3.client('ses',region_name=AWS_REGION)
    response = ses_client.send_raw_email(
        Source=SENDER,
        Destinations=[RECIPIENT],
        RawMessage={'Data': message}
    )


def main():
    s3_client = boto3.client("s3")
    list_objects = s3_client.list_objects(Bucket=bucket_name)
    contents = list_objects["Contents"]
    email_list = []

    for content in contents:
        key_id = content["Key"]
        email_list.append(key_id)
        response = s3_client.get_object(Bucket=bucket_name, Key=key_id)
        raw_message = response['Body'].read()
        send_mail(raw_message)

def lambda_handler(event, context):
    main()

