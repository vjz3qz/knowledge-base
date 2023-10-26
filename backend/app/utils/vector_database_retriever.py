# Utility functions for creating, updating, and querying the FAISS index.

import os
import sys
from .generate_unique_id import generate_unique_id
from .document_retriever import get_metadata_from_s3, get_url_from_s3

import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain

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


def add_text_to_chroma(texts, file_id):
    # Step 1: Generate unique ID

    # Chunk/Page Level Hash
    chunk_ids = [generate_unique_id(chunk) for chunk in texts]

    # TODO Step 2: Check for duplicates
    for id in chunk_ids:
        existing_doc = chroma_db._collection.get(ids=[id])
        if existing_doc.get('documents'):
            print(f"Document with ID {id} already exists.")
            return

    # TODO USE unique identifier for source, that way we can fetch the data and display it to user
    sources = [{"source": file_id, "text": f"{chunk}", "chunk_id": f"{id}"}
               for chunk, id in zip(texts, chunk_ids)]

    # Step 3: Embed and store the document
    chroma_db.from_texts(texts, embedding, metadatas=sources,
                         ids=chunk_ids, persist_directory=PERSISTENT_DIRECTORY)
    print(f"Document added successfully.")


def search_in_chroma(query, chroma_db=None):
    if not chroma_db:
        chroma_db = Chroma(
            persist_directory=PERSISTENT_DIRECTORY, embedding_function=embedding)
    qa = RetrievalQAWithSourcesChain.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=chroma_db.as_retriever())
    return qa({"question": query}, return_only_outputs=True)


def search_k_in_chroma(query, k=3, chroma_db=None):
    if not chroma_db:
        chroma_db = Chroma(
            persist_directory=PERSISTENT_DIRECTORY, embedding_function=embedding)
    retriever = chroma_db.as_retriever(search_kwargs={"k": k})
    # docs = retriever.get_relevant_documents(query)
    qa = RetrievalQAWithSourcesChain.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=retriever, return_source_documents=True)

    qa_response = qa(query)
    sources = [source.metadata['source']
               for source in qa_response['source_documents']]
    source_data = {source: {"url": get_url_from_s3(source), "metadata": get_metadata_from_s3(
        source)} for source in sources}
    response = {"answer": qa_response['answer'], "sources": source_data}
    return response
