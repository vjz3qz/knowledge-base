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

def add_file(file_object, file_id, media_id, file_type, text=""):
    """
    Uploads a file to the specified S3 bucket.
    :param file_object: The file object to upload.
    :param file_id: The ID (filename) for the file in S3.
    :param media_id: Which media object the file should be stored under.
    :param file_type: The type of file being uploaded (image, video, document, etc.)
    :return: The file ID if successful, or an error message.
    """
    try:
        if file_type == 'video' or file_type == 'image':
            key = get_text_file_path(file_id, media_id, file_type)
            s3.upload_fileobj(Fileobj=text, Bucket=bucket_name, Key=key)
        key = get_file_path(file_id, media_id, file_type)
        s3.upload_fileobj(Fileobj=file_object, Bucket=bucket_name, Key=key)
        # TODO return confirmation code
        return file_id
    except NoCredentialsError:
        return "Credentials not available"

def get_file(file_id, media_id, file_type):
    """
    Generates a presigned URL for a file in S3.
    :param file_id: The ID (filename) of the file in S3.
    :param media_id: Which media object the file is be stored under.
    :param file_type: The type of file being retrieved (image, video, document, etc.)
    :return: A presigned URL if successful, or an error message.
    """
    try:
        key = get_file_path(file_id, media_id, file_type)
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key}, ExpiresIn=3600)
        return url
    except NoCredentialsError:
        return "Credentials not available"

def get_text_file(file_id, media_id, file_type):
    """
    Retrieves a text file from S3.
    :param file_id: The ID (filename) of the file in S3.
    :param media_id: Which media object the file is be stored under.
    :param file_type: The type of file being retrieved (image, video, document, etc.)
    :return: The text file if successful, or an error message.
    """
    try:
        key = get_text_file_path(file_id, media_id, file_type)
        url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': key}, ExpiresIn=3600)
        return url
    except NoCredentialsError:
        return "Credentials not available"

def get_file_path(file_id, media_id, file_type):
    """
    Retrieves the path for a file in S3.
    :param file_id: The ID (filename) of the file in S3.
    :param media_id: Which media object the file is be stored under.
    :param file_type: The type of file being retrieved (image, video, document, etc.)
    :return: The path for the file.
    """
    key = f"{media_id}/{file_type}/{file_id}"
    if file_type == 'video' or file_type == 'image':
        key = f"{media_id}/{file_type}/{file_type}/{file_id}"
    return key

def get_text_file_path(file_id, media_id, file_type):
    """
    Retrieves the path for a text file in S3.
    :param file_id: The ID (filename) of the file in S3.
    :param media_id: Which media object the file is be stored under.
    :param file_type: The type of file being retrieved (image, video, document, etc.)
    :return: The path for the text file.
    """
    key = f"{media_id}/{file_type}/{file_id}"
    if file_type == 'video':
        key = f"{media_id}/{file_type}/transcript/{file_id}"
    elif file_type == 'image':
        key = f"{media_id}/{file_type}/summary/{file_id}"
    return key