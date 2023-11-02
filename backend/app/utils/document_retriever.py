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


def upload_document_to_s3(file, unique_id, file_name="", summary=""):
    if not file_name:
        file_name = unique_id
    
    # Metadata
    metadata = {
        'name': file_name,
        'summary': summary
    }
    res = get_file_extension(file_name)[0]
    content_type = res if res else 'application/octet-stream'

    # Upload to S3 using the hash as the key
    s3.upload_fileobj(
        Fileobj=file,
        Bucket=bucket_name,
        Key=unique_id,
        ExtraArgs={'Metadata': metadata, 'ContentType': content_type}
    )

    return unique_id



def upload_image_to_s3(image, unique_id, image_name="", bucket=bucket_name, prefix = ""):
    if not image_name:
        image_name = unique_id
    
    if prefix:
        key = prefix + "/" + unique_id
    else:
        key = unique_id
    # Metadata
    metadata = {
        'name': image_name,
    }

    type, extension = get_file_extension(image_name)
    content_type = type if type else "binary/octet-stream"


    # Upload to S3 using the hash as the key
    s3.upload_fileobj(
        Fileobj=image,
        Bucket=bucket,
        Key=key,
        ExtraArgs={'Metadata': metadata, 'ContentType': content_type}
    )

    return unique_id


def get_metadata_from_s3(unique_id):
    
    response = s3.head_object(Bucket=bucket_name, Key=unique_id)
    metadata = response['Metadata']
    
    return metadata


def get_url_from_s3(unique_id, bucket=bucket_name, prefix = ""):
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

def call_lambda_function(image_id, content_type, file_extension):
    response = lambda_client.invoke(
        FunctionName='yolov5-lambda',
        InvocationType='RequestResponse',  # Synchronous invocation
        Payload=json.dumps({
            'image_id': image_id,
            'content_type': content_type,
            'file_extension': file_extension
            # 's3_url': 'https://s3-your-region.amazonaws.com/your-bucket-name/your-image-path.jpg'
        })
    )

    lambda_response = json.loads(response['Payload'].read())
    # body_content = json.loads(lambda_response.get('body', '{}'))
    return lambda_response
