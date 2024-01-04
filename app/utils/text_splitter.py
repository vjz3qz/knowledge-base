from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import S3FileLoader

def load_and_split(file_id, media_id, file_type):
    # load from s3
    loader = S3FileLoader(media_id + "/" + file_type, file_id)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    return text_splitter.split_documents(documents)

# aws_access_key_id="xxxx", aws_secret_access_key="yyyy" as params if not env vars

# TODO ADD SUPPORT FOR IMAGE SUMMARIES AND VIDEO TRANSCRIPTS