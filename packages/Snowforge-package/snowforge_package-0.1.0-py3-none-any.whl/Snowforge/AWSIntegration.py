import os
import boto3
from boto3.s3.transfer import TransferConfig
import json
from tqdm import tqdm
from .Logging import Debug  # Import logging class

class ProgressPercentage:
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._tqdm = tqdm(total=self._size, unit='B', unit_scale=True, desc=filename)

    def __call__(self, bytes_amount):
        self._seen_so_far += bytes_amount
        self._tqdm.update(bytes_amount)

class AWSIntegration:
    """Static AWS Helper Class for managing S3 and Secrets Manager operations."""

    s3_client = None
    secret_client = None

    @staticmethod
    def initialize():
        """Initializes AWS clients for S3 and Secrets Manager.

        If credentials are missing, prompts the user for input. If authentication
        fails, resets credentials so that `initialize()` can be called again for reattempt.

        Raises:
            Exception: If AWS authentication fails.
        """

        # If already initialized successfully, return
        if AWSIntegration.s3_client is not None and AWSIntegration.secret_client is not None:
            return  

        # Get credentials from environment variables
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

        # If credentials are missing, prompt the user
        if not access_key or not secret_key:
            access_key = input("Please enter your AWS access key: ")
            secret_key = input("Please enter your AWS secret: ")

            # Temporarily store them (but DO NOT set in os.environ to avoid persistence issues)
            os.environ["AWS_ACCESS_KEY_ID"] = access_key
            os.environ["AWS_SECRET_ACCESS_KEY"] = secret_key

        try:
            AWSIntegration.s3_client = boto3.client(
                "s3",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name="eu-north-1",
            )

            AWSIntegration.secret_client = boto3.client(
                "secretsmanager",
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name="eu-north-1",
            )

            # 🔥 Perform a real AWS call to validate credentials
            AWSIntegration.s3_client.list_buckets()

            Debug.log("Connected to AWS!", "INFO")

        except Exception as e:

            # Reset class variables to allow retrying on next call
            AWSIntegration.s3_client = None
            AWSIntegration.secret_client = None

            # Reset environment variables (so `initialize()` prompts again on next call)
            os.environ.pop("AWS_ACCESS_KEY_ID", None)
            os.environ.pop("AWS_SECRET_ACCESS_KEY", None)

            Debug.log("\n\n❌ Invalid AWS credentials! Set the 'AWS_ACCESS_KEY_ID' and the 'AWS_SECRET_ACCESS_KEY' correctly.\n", 'ERROR')

    @staticmethod
    def define_s3_transfer_config(size_threshold: float, threads: int):
        """Defines and returns an AWS S3 TransferConfig for efficient file uploads.

        Args:
            size_threshold (float): The file size (in GB) at which multipart upload should trigger.
            threads (int): Number of concurrent threads for upload.

        Returns:
            TransferConfig: Configured transfer settings for AWS S3 uploads.
        """
        GB = 1024 ** 3
        Debug.log(f"Threshold for multithreaded upload to S3: {size_threshold}GB\n"
                f"Concurrent threads: {threads}", 'INFO')

        return TransferConfig(multipart_threshold=size_threshold * GB, max_concurrency=threads)

    @staticmethod
    def get_secret(secret_name: str):
        """Retrieves a secret from AWS Secrets Manager.

        Args:
            secret_name (str): The name of the secret to retrieve.

        Returns:
            dict: The secret's value parsed as a dictionary.

        Raises:
            Exception: If retrieval fails.
        """
        AWSIntegration.initialize()
        try:
            response = AWSIntegration.secret_client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except Exception as e:
            Debug.log(f"Failed to retrieve secret: {e}", 'ERROR')

    @staticmethod
    def get_bucket_contents(bucket_name: str):
        """Lists all files in a given AWS S3 bucket.

        Args:
            bucket_name (str): The name of the S3 bucket.

        Returns:
            list[str]: A list of filenames stored in the bucket.

        Raises:
            Exception: If the bucket is not accessible.
        """
        AWSIntegration.initialize()
        try:
            response = AWSIntegration.s3_client.list_objects_v2(Bucket=bucket_name)
            return [item['Key'] for item in response.get('Contents', [])]
        except Exception as e:
            Debug.log(f"Error fetching bucket contents: {e}", 'ERROR')

    @staticmethod
    def push_file_to_s3(bucket_name: str, file_to_upload: str, key: str, config: TransferConfig = None):
        """Uploads a file to an AWS S3 bucket.

        Args:
            bucket_name (str): The destination S3 bucket name.
            file_to_upload (str): Path to the file to upload.
            key (str): The S3 key (filename) to assign.
            config (TransferConfig, optional): AWS S3 transfer configuration. Defaults to None.

        Raises:
            Exception: If the upload fails.
        """
        AWSIntegration.initialize()

        if config is None:
            config = AWSIntegration.define_s3_transfer_config(0.1, 10)

        try:
            Debug.log(f"Uploading {file_to_upload} to {bucket_name}/{key}...", 'INFO')

            with open(file_to_upload, 'rb') as file_obj:
                AWSIntegration.s3_client.upload_fileobj(
                    file_obj, bucket_name, key, Config=config, Callback=ProgressPercentage(file_to_upload)
                )

            Debug.log(f"Successfully uploaded {file_to_upload} to {bucket_name}/{key}", 'SUCCESS')

        except Exception as e:
            Debug.log(f"Error uploading file: {e}", 'ERROR')
