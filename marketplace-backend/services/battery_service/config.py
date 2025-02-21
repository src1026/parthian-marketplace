import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")
