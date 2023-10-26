from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader

def extract_text_from_stream(byte_stream):
    # TODO add support for other document types
    # TODO don't chunk mid sentence
    reader = PdfReader(byte_stream)

    text = str()
    # Extract text
    for page in reader.pages:
        text += page.extract_text()
    return text

def chunk_text(text):
    # TODO don't chunk mid sentence
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(text)