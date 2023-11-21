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
# persistent_client.reset()
chroma_db = Chroma(client=persistent_client)


def add_text_to_chroma(texts, file_id, time_stamps=None):
    # Step 1: Generate unique ID
    chunk_ids = create_chunk_ids(texts)

    # Step 2: Check for duplicates
    # TODO update to file_id, but also need to maintain unique chunk_ids?
    for id in chunk_ids:
        existing_doc = chroma_db._collection.get(ids=[id])
        if existing_doc.get('documents'):
            print(f"Document with ID {id} already exists.")
            return

    create_sources(texts, file_id, chunk_ids, time_stamps)
    embed_to_chroma(texts, sources, chunk_ids)

def create_chunk_ids(texts):
    # Chunk/Page Level Hash
    return [generate_unique_id(chunk) for chunk in texts]

def create_sources(texts, file_id, chunk_ids, time_stamps=None):
    if time_stamps:
        return [{"source": file_id, "text": f"{chunk}", "chunk_id": f"{chunk_id}", "time_stamp": time_stamp}
               for chunk, chunk_id, time_stamp in zip(texts, chunk_ids, time_stamps)]
    else:
        return [{"source": file_id, "text": f"{chunk}", "chunk_id": f"{chunk_id}"}
               for chunk, chunk_id in zip(texts, chunk_ids)]
    

def embed_to_chroma(texts, sources, chunk_ids):
    # Step 3: Embed and store the document
    try:
        chroma_db.from_texts(texts, embedding, metadatas=sources,
                            ids=chunk_ids, persist_directory=PERSISTENT_DIRECTORY)
        print(f"Document added successfully.")
    except Exception as e:
        print(e)


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
    source_data = {}
    for source in qa_response['source_documents']:
        source = source.metadata['source']
        time_stamp =  source.metadata['time_stamp'] if 'time_stamp' in source.metadata else None
        source_data[source] = {"url": get_url_from_s3(source), "metadata": get_metadata_from_s3(
            source)}
        if time_stamp:
            source_data[source]['time_stamp'] = time_stamp
    response = {"answer": qa_response['answer'], "sources": source_data}
    # TODO add time stamp support in frontend
    return response
