from io import BytesIO
from typing import Optional

import boto3
from PIL import Image


class AWSS3:
    """
    AWS S3 client to upload and download images.
    """

    def __init__(
        self,
        bucket_name: str,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        region_name: str,
    ):
        """
        Create S3 client and set bucket name.
        """
        self.s3 = boto3.client(
            "s3",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
        self.bucket_name = bucket_name

    def upload_image(self, image: Image, s3_key: str) -> bool:
        """
        Upload image to S3 bucket and return S3 key.

        :param image: Image to upload
        :param s3_key: S3 key of image

        :return: S3 key of image
        """
        try:
            with BytesIO() as output:
                image.save(output, format="JPEG")
                output.seek(0)
                self.s3.upload_fileobj(output, self.bucket_name, s3_key)

            return True

        except Exception as e:
            print(f"error uploading image to s3: {e}")
            return False

    def download_image(self, s3_key: str) -> Optional[Image]:
        """
        Download image from S3 bucket.

        :param s3_key: S3 key of image

        :return: Image
        """

        try:
            with BytesIO() as output:
                self.s3.download_fileobj(self.bucket_name, s3_key, output)
                output.seek(0)
                image = Image.open(output)

            return image

        except Exception as e:
            print(f"error downloading image from s3: {e}")
            return None
