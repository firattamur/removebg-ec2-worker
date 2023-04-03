import os

import dotenv

# Load environment variables from .env file in root directory
dotenv.load_dotenv()

# AWS Credetials
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")

# AWS S3
AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")

# AWS SQS
AWS_SQS_QUEUE_NAME = os.environ.get("AWS_SQS_QUEUE_NAME")
AWS_SNS_TOPIC_NAME = os.environ.get("AWS_SNS_TOPIC_NAME")
