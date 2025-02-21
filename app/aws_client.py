# app/aws_client.py
import boto3
import logging
from botocore.exceptions import (
    NoCredentialsError,
    PartialCredentialsError,
    EndpointConnectionError,
)
from .config import REGION_NAME, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def initialize_firehose_client():
    try:
        return boto3.client(
            "firehose",
            region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        logging.critical(f"Invalid AWS credentials: {e}")
        exit(1)
    except EndpointConnectionError as e:
        logging.critical(f"Unable to connect to AWS: {e}")
        exit(1)


firehose_client = initialize_firehose_client()
