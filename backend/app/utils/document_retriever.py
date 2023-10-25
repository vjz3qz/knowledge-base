# Utility functions for uploading and retrieving files from S3.
import sys
import os
import boto3
import uuid
from io import BytesIO
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

try:  
  os.environ['S3_BUCKET_NAME']
except KeyError: 
  print('[error]: `S3_BUCKET_NAME` environment variable required')
  sys.exit(1)

bucket_name = os.environ.get('S3_BUCKET_NAME')
s3 = boto3.client('s3')


def upload_to_s3(file, unique_id=None, file_name="", summary=""):
    if not unique_id:
        # Generate UUID
        unique_id = str(uuid.uuid4())
    if not file_name:
        file_name = unique_id
    
    # Metadata
    metadata = {
        'name': file_name,
        'summary': summary
    }

    # Upload to S3 using the UUID as the key
    s3.upload_fileobj(
        Fileobj=file,
        Bucket=bucket_name,
        Key=unique_id,
        ExtraArgs={'Metadata': metadata}
    )

    return unique_id


def get_metadata_from_s3(unique_id):
    
    response = s3.head_object(Bucket=bucket_name, Key=unique_id)
    metadata = response['Metadata']
    
    return metadata


def get_url_from_s3(unique_id):
    # Generate the S3 URL for downloading the file (URL will expire after 1 hour)
    url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': unique_id}, ExpiresIn=3600)
    # file = s3.get_object(Bucket=bucket_name, Key=unique_id)
    # return file['Body'].read()
    return url


def extract_text_from_s3(unique_id, bucket_name):
    # Step 1 & 2: Fetch the file from S3 into a bytes buffer
    s3_response_object = s3.get_object(Bucket=bucket_name, Key=unique_id)
    pdf_file = BytesIO(s3_response_object['Body'].read())

    # Step 3: Use the bytes buffer with PyPDFLoader
    loader = PyPDFLoader(pdf_file)
    pages = loader.load_and_split()
    combined_content = ''.join([p.page_content for p in pages])
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(combined_content)
