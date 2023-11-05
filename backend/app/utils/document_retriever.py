# Utility functions for uploading and retrieving files from S3.
import sys
import os
from .document_processor import extract_text_from_stream
import boto3
from io import BytesIO
import json
from .document_processor import get_file_extension

try:  
  os.environ['S3_BUCKET_NAME']
except KeyError: 
  print('[error]: `S3_BUCKET_NAME` environment variable required')
  sys.exit(1)

bucket_name = os.environ.get('S3_BUCKET_NAME')
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

# file, file_id, metadata, content_type, bucket_name, prefix = ""
def upload_document_to_s3(file, file_id, metadata = {}, content_type = "", bucket = bucket_name, prefix = ""):

    if not content_type:
        res = get_file_extension(file_id)[0]
        content_type = res if res else 'application/octet-stream'
    
    if prefix:
        key = prefix + "/" + file_id
    else:
        key = file_id

    # Metadata
    final_metadata = {}
    if 'name' in metadata:
        final_metadata['name'] = metadata['name']
    if 'summary' in metadata:
        final_metadata['summary'] = metadata['summary']
    if 'file_type' in metadata:
        final_metadata['file_type'] = metadata['file_type']
    if 'content_type' in metadata:
        final_metadata['content_type'] = metadata['content_type']

    # Upload to S3 using the hash as the key
    s3.upload_fileobj(
        Fileobj=file,
        Bucket=bucket,
        Key=key,
        ExtraArgs={'Metadata': final_metadata, 'ContentType': content_type}
    )

    return file_id


def get_metadata_from_s3(unique_id):
    
    response = s3.head_object(Bucket=bucket_name, Key=unique_id)
    metadata = response['Metadata']
    
    return metadata


def get_url_from_s3(unique_id, bucket=bucket_name, prefix = ""):
    if not bucket:
        bucket = bucket_name
    if prefix:
        key = prefix + "/" + unique_id
    else:
        key = unique_id
    # Generate the S3 URL for downloading the file (URL will expire after 1 hour)
    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=3600)
    # file = s3.get_object(Bucket=bucket_name, Key=unique_id)
    # return file['Body'].read()
    return url


def extract_text_from_s3(unique_id):
    # Step 1 & 2: Fetch the file from S3 into a bytes buffer
    s3_response_object = s3.get_object(Bucket=bucket_name, Key=unique_id)
    pdf_file = BytesIO(s3_response_object['Body'].read())
    return extract_text_from_stream(pdf_file)


client = boto3.client('lambda')

def call_lambda_function(image_id):
    response = lambda_client.invoke(
        FunctionName='yolov5-lambda',
        InvocationType='RequestResponse',  # Synchronous invocation
        Payload=json.dumps({
            'image_id': image_id
        })
    )

    lambda_response = json.loads(response['Payload'].read())
    # body_content = json.loads(lambda_response.get('body', '{}'))
    return lambda_response
