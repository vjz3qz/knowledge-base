# AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are defined in the environmentimport sys
import os
import boto3
from botocore.exceptions import NoCredentialsError

# Check for required environment variable
try:  
    bucket_name = os.environ['S3_BUCKET_NAME']
except KeyError: 
    raise EnvironmentError('[error]: `S3_BUCKET_NAME` environment variable required')


s3 = boto3.client('s3')

def add_file(file_object, file_id, media_id, file_type):
    """
    Uploads a file to the specified S3 bucket.
    :param file_object: The file object to upload.
    :param file_id: The ID (filename) for the file in S3.
    :param media_id: Which media object the file should be stored under.
    :param file_type: The type of file being uploaded (image, video, document, etc.)
    :return: The file ID if successful, or an error message.
    """
    try:
        key = f"{prefix}/{file_id}" if prefix else file_id
        s3.upload_fileobj(Fileobj=file_object, Bucket=bucket_name, Key=key)
        return file_id
    except NoCredentialsError:
        return "Credentials not available"

def get_url_from_s3(file_id, media_id, file_type):
    """
    Generates a presigned URL for a file in S3.
    :param file_id: The ID (filename) of the file in S3.
    :param media_id: Which media object the file is be stored under.
    :param file_type: The type of file being retrieved (image, video, document, etc.)
    :return: A presigned URL if successful, or an error message.
    """
    try:
        key = f"{prefix}/{file_id}" if prefix else file_id
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key}, ExpiresIn=3600)
        return url
    except NoCredentialsError:
        return "Credentials not available"
