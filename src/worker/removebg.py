import json

import boto3
from rembg import remove

from .awss3 import AWSS3
from .config import (
    AWS_ACCESS_KEY_ID,
    AWS_DEFAULT_REGION,
    AWS_S3_BUCKET_NAME,
    AWS_SECRET_ACCESS_KEY,
    AWS_SNS_TOPIC_NAME,
    AWS_SQS_QUEUE_NAME,
)


class RemoveBG:
    """
    Remove background from image.
    This class is used to run the remove background and upload the image to S3.
    """

    def __init__(self):
        """
        Initialize RemoveBG class.

        :param s3_key: S3 key of image
        """
        self.awss3 = AWSS3(
            AWS_S3_BUCKET_NAME,
            AWS_ACCESS_KEY_ID,
            AWS_SECRET_ACCESS_KEY,
            AWS_DEFAULT_REGION,
        )

        self.sqs = boto3.client(
            "sqs",
            region_name=AWS_DEFAULT_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

        self.sns = boto3.client(
            "sns",
            region_name=AWS_DEFAULT_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )

    def remove_background(self, s3_key_original: str):
        """
        Remove background from image

        :param s3_key_original: S3 key of original image
        :return: S3 key of image without background
        """

        # Download image from S3
        image = self.awss3.download_image(s3_key_original)

        # Remove background from image
        removed_bg_image = remove(image)

        # Create new S3 key
        s3_key_processed = s3_key_original.replace("original", "processed")

        # Upload image to S3
        self.awss3.upload_image(removed_bg_image, s3_key_processed)

        return s3_key_processed

    def run(self):
        """
        Run remove background worker. This method will poll for messages in the SQS queue.
        When a message is received, it will process the image and publish a message to SNS.

        :return: None
        """

        while True:
            try:
                # Poll for messages
                response = self.sqs.receive_message(
                    QueueUrl=AWS_SQS_QUEUE_NAME,
                    MaxNumberOfMessages=1,
                    WaitTimeSeconds=20,
                )

                # If not messages, continue
                if "Messages" not in response:
                    print("No messages in the queue, waiting...")
                    continue

                # Get message
                message = response["Messages"][0]
                message_json = json.loads(message["Body"])

                # Extract S3 key and request ID from message body
                s3_key_original = message_json["s3_key_original"]
                request_id = message_json["request_id"]

                # Process image
                print(f"Processing image {s3_key_original}...")
                s3_key_processed = self.remove_background(s3_key_original)

                # Publish message to SNS
                print("Publishing message to SNS...")
                self.sns.publish(
                    TopicArn=AWS_SNS_TOPIC_NAME,
                    Message=f"{s3_key_processed}, {request_id}",
                )

                # Delete message from SQS
                print("Deleting message from SQS...")
                self.sqs.delete_message(
                    QueueUrl=AWS_SQS_QUEUE_NAME, ReceiptHandle=message["ReceiptHandle"]
                )

            except Exception as e:
                print("error processing image: ", e)
                continue
