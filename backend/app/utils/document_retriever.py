# Utility functions for uploading and retrieving files from S3.
import sys
import os
from .document_processor import extract_text_from_stream
import boto3
from io import BytesIO
import json

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

    content_type = 'application/pdf' if file_name.lower().endswith('.pdf') else 'application/octet-stream'

    # Upload to S3 using the hash as the key
    s3.upload_fileobj(
        Fileobj=file,
        Bucket=bucket_name,
        Key=unique_id,
        ExtraArgs={'Metadata': metadata, 'ContentType': content_type}
    )

    return unique_id


def upload_image_to_s3(image, unique_id, image_name=""):
    if not image_name:
        image_name = unique_id
    
    # Metadata
    metadata = {
        'name': image_name,
    }

    content_type_map = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        # add other image types if needed
    }
    file_extension = os.path.splitext(image_name)[1][1:]  # Get extension without the dot
    content_type = content_type_map.get(file_extension, "binary/octet-stream")


    # Upload to S3 using the hash as the key
    s3.upload_fileobj(
        Fileobj=image,
        Bucket=bucket_name,
        Key=unique_id,
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

def call_lambda_function(s3_url):
    response = lambda_client.invoke(
        FunctionName='yolov5-lambda',
        InvocationType='RequestResponse',  # Synchronous invocation
        Payload=json.dumps({
            's3_url': s3_url
            # 's3_url': 'https://s3-your-region.amazonaws.com/your-bucket-name/your-image-path.jpg'
        })
    )

    lambda_response = json.loads(response['Payload'].read())
    body_content = json.loads(lambda_response.get('body', '{}'))
    return body_content
