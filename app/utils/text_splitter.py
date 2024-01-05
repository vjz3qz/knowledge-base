from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import S3FileLoader
from app.services.blob_storage_service import get_text_file_path

# Check for required environment variable
try:  
    bucket_name = os.environ['S3_BUCKET_NAME']
except KeyError: 
    raise EnvironmentError('[error]: `S3_BUCKET_NAME` environment variable required')

def load_and_split(file_id, media_id, file_type):
    # load from s3
    key = get_text_file_path(file_id, media_id, file_type)
    loader = S3FileLoader(bucket_name, key)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)

# aws_access_key_id="xxxx", aws_secret_access_key="yyyy" as params if not env vars