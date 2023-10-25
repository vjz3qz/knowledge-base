# Utility functions for creating, updating, and querying the FAISS index.

import os
import sys
import uuid
import hashlib
import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
# import langchain.chains.VectorDBQAWithSourcesChain

try:  
  os.environ['OPENAI_API_KEY']
except KeyError: 
  print('[error]: `OPENAI_API_KEY` environment variable required')
  sys.exit(1)

api_key = os.environ.get('OPENAI_API_KEY')
embedding = OpenAIEmbeddings(openai_api_key=api_key)


# We assume you've already initialized Chroma DB before
PERSISTENT_DIRECTORY = "../vector_database/chroma_db"

persistent_client = chromadb.PersistentClient(path=PERSISTENT_DIRECTORY)
chroma_db = Chroma(client=persistent_client)

def generate_unique_id(document_content):
    # Here, we're using a hash of the document content as its unique ID
    # return hashlib.sha256(document_content.encode()).hexdigest()
    # TODO USE HASH instead of UUID
    return str(uuid.uuid4())

def add_text_to_chroma(text, doc_id=None):
    # Step 1: Generate unique ID
    if not doc_id:
        doc_id = generate_unique_id(text)

    # TODO Step 2: Check for duplicates
    existing_doc = chroma_db._collection.get(ids=[doc_id])
    if existing_doc['documents']:
        print(f"Document with ID {doc_id} already exists.")
        return
    
    # TODO USE unique identifier for source, that way we can fetch the data and display it to user
    sources = [{"source": f"{i}-pl"} for i in range(len(text))]

    # Step 3: Embed and store the document
    chroma_db.from_texts(text, embedding, metadatas=sources, ids=doc_id, persist_directory=PERSISTENT_DIRECTORY)
    # chroma_db.persist()
    print(f"Document with ID {doc_id} added successfully.")

# # Test
# document = "This is a test document."
# add_document_to_chroma(document)

def search_in_chroma(query):
    chroma_db = Chroma(persist_directory=PERSISTENT_DIRECTORY, embedding_function=embedding)
    qa = RetrievalQAWithSourcesChain.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=chroma_db.as_retriever())
    return qa({"question": query}, return_only_outputs=True)



