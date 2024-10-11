import boto3
from src.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

def init_aws_client():
    return boto3.client(service_name='comprehend', 
                        region_name=AWS_REGION, 
                        aws_access_key_id=AWS_ACCESS_KEY_ID, 
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

comprehend = init_aws_client()