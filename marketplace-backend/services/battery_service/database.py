import boto3
from config import AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, DYNAMODB_TABLE_NAME
from fastapi import APIRouter, UploadFile, File, HTTPException

dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

battery_table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def create_table():
    try:
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE_NAME,
            KeySchema=[{"AttributeName": "batteryId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "batteryId", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
        )
        table.wait_until_exists()
        print(f"Table {DYNAMODB_TABLE_NAME} created successfully!")
    except Exception as e:
        print(f"Table already exists or error: {e}")

create_table()

S3_BUCKET = "battery-img"
S3_REGION = "us-east-1"

s3_client = boto3.client(
    "s3",
    region_name=S3_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)