from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

def extract_text(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    combined_content = ''.join([p.page_content for p in pages])
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=200, length_function=len)
    return text_splitter.split_text(combined_content)