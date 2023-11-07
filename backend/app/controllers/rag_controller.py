# Description: Controller for RAG model
from app.utils.query_document import query_document
from app.utils.summarize_document import summarize_document
from app.utils.document_processor import chunk_text
from app.utils.document_retriever import extract_text_from_s3


def rag_handler(current_message, file_id, intent, llm, file_type):
    if file_type not in ['text', 'diagram']:
        return {"Error": "Invalid file type"}
        
    if file_type == 'text':
        text = extract_text_from_s3(file_id)

    elif file_type == 'diagram':
        # use metadata for now
        metadata = get_metadata_from_s3(file_id)
        summary = metadata['summary']
        symbol_summary = metadata['symbol_summary']
        text = summary + symbol_summary

    chunks = chunk_text(text)

    if intent == 'question':
        response = query_document(current_message, chunks, llm)

    elif intent == 'summarize':
        response = summarize_document(chunks, llm)

    return response