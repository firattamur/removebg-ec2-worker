import os

from dotenv import load_dotenv

# Load environment variables from .env file in root directory
load_dotenv(".env.local")

# AWS Credetials
AWS_ACCESS_KEY_ID = os.environ.get("APP_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("APP_AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.environ.get("APP_AWS_DEFAULT_REGION")

# AWS S3
AWS_S3_BUCKET_NAME = os.environ.get("APP_AWS_BUCKET_NAME")

# AWS SQS
AWS_SQS_QUEUE_NAME = os.environ.get("APP_AWS_SQS_QUEUE_URL")
AWS_SNS_TOPIC_NAME = os.environ.get("APP_AWS_SNS_TOPIC_ARN")
