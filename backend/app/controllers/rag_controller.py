# Description: Controller for RAG model
from app.utils.query_document import query_document
from app.utils.summarize_document import summarize_document
from app.utils.document_processor import chunk_text
from app.utils.document_retriever import extract_text_from_s3, get_metadata_from_s3, get_url_from_s3
from app.utils.diagram_parser import deserialize_from_json
import requests


def rag_handler(current_message, file_id, intent, llm, file_type):
    if file_type not in ['text', 'diagram']:
        return {"Error": "Invalid file type"}

    if file_type == 'text':
        text = extract_text_from_s3(file_id)

    elif file_type == 'diagram':
        # use metadata for now
        metadata = get_metadata_from_s3(file_id)
        url = get_url_from_s3(file_id, bucket='trace-ai-diagram-metadata')
        response = requests.get(url)
        if response.status_code == 200:
            summary = deserialize_from_json(response.json())[-1] # get file name from first element
        else:
            print("Failed to get data:", response.status_code)
            summary = ''
        symbol_summary = metadata['summary']
        text = summary + symbol_summary # TODO potentially add file name

    chunks = chunk_text(text)

    if intent == 'question':
        response = query_document(current_message, chunks, llm)

    elif intent == 'summarize':
        response = summarize_document(chunks, llm)

    return response