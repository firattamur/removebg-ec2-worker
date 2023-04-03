# 🖼️ Image Background Removal Worker 👷‍♂️

This repository contains the code for the EC2 worker component of the Image Background Removal Service. The worker is responsible for processing images by removing their backgrounds. The following steps outline the process:

1. The worker listens for messages from an Amazon SQS queue.
2. Each message contains the S3 object key of the image to be processed.
3. The worker downloads the image from the S3 bucket using the object key.
4. It removes the background from the image using a background removal algorithm.
5. The processed image is uploaded back to the S3 bucket.
6. Once the processing is complete, the worker sends a message to an Amazon SNS topic.
7. The FastAPI backend is subscribed to the SNS topic and gets notified that the processed image is available.

## 🚀 Getting Started

1. Clone this repository.
2. Create a virtual environment and activate it by running

```bash
python -m venv venv && source venv/bin/activate
```

3. Install the required Python dependencies by running

```bash
pip install -r requirements.txt
```

4. Create a file named .env in the root directory of your project.
5. Add the following lines to the .env file:

```bash
AWS_ACCESS_KEY_ID=<your-aws-access-key-id>
AWS_SECRET_ACCESS_KEY=<your-aws-secret-access-key>
AWS_REGION=<your-aws-region>
SNS_TOPIC_ARN=<your-sns-topic-arn>
SQS_QUEUE_URL=<your-sqs-queue-url>
S3_BUCKET_NAME=<your-s3-bucket-name>
```

5. Run the following command to process images from SQS and SNS:

```bash
python src/main.py
```

This script will continuously poll the SQS queue for messages and process the images in the messages. To test if the script is working correctly, you can send a message to the SQS queue with an S3 object key and a request ID, and check if the processed image is uploaded to the S3 bucket and a message is published to the SNS topic with the processed image's S3 key and request ID.

## 📦 Deployment

This project uses GitHub Actions for CI/CD. To build and deploy the custom AMI:

1. Push changes to the main branch of this repository.
2. The GitHub Actions workflow defined in `.github/workflows/main.yml` will automatically build a new AMI using Packer and the configuration in the `packer/` directory.
3. Once the AMI is built, you can update the Auto Scaling group to use the new AMI for launching new instances.

## 📚 Documentation

For more information on how this worker fits into the overall Image Background Removal Service, please refer to the [FastAPI backend repository](https://github.com/your-username/backend-project-name).

## 🤝 Contributing

Contributions are more than welcome! If you find any issues, have suggestions for improvements, or would like to add new design pattern examples, please open an issue or submit a pull request.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
