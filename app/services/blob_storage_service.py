# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are defined in the environment
import sys
import os
import boto3
from botocore.exceptions import NoCredentialsError

try:  
  os.environ['S3_BUCKET_NAME']
except KeyError: 
  print('[error]: `S3_BUCKET_NAME` environment variable required')
  sys.exit(1)

bucket_name = os.environ.get('S3_BUCKET_NAME')
s3 = boto3.client('s3')

def add_file(file_object, file_id, prefix = ""):
    try:
        if prefix:
            key = prefix + "/" + file_id
        else:
            key = file_id


        # Upload to S3 using the hash as the key
        s3.upload_fileobj(
            Fileobj=file_object,
            Bucket=bucket,
            Key=key,
        )

        return file_id
    except NoCredentialsError:
        return "Credentials not available"


def get_url_from_s3(file_id, prefix = ""):
    try:
        if not bucket:
            bucket = bucket_name
        if prefix:
            key = prefix + "/" + file_id
        else:
            key = file_id
        # Generate the S3 URL for downloading the file (URL will expire after 1 hour)
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=3600)
        return url
    except NoCredentialsError:
        return "Credentials not available"