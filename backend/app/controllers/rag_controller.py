# Description: Controller for RAG model
from app.utils.query_document import query_document
from app.utils.summarize_document import summarize_document
from app.utils.document_processor import chunk_text
from app.utils.document_retriever import extract_text_from_s3, extract_image_summary_from_s3, extract_table_text_from_s3


def rag_handler(current_message, file_id, intent, llm, file_type):
    if file_type == 'text':
        response = text_rag_handler(current_message, file_id, intent, llm)
    elif file_type == 'diagram':
        response = diagram_rag_handler(current_message, file_id, intent, llm)
    else:
        response = {"Error": "Invalid file type"}

    return response

def text_rag_handler(current_message, file_id, intent, llm):
    texts = extract_text_from_s3(file_id)
    chunks = chunk_text(texts)

    if intent == 'question':
        response = query_document(current_message, chunks, llm)

    elif intent == 'summarize':
        response = summarize_document(chunks, llm)

    return response

def diagram_rag_handler(current_message, file_id, intent, llm):
    return "test"
    image_summary = extract_image_summary_from_s3(file_id)
    table_text = extract_table_text_from_s3(file_id)

    if intent == 'question':
        response = query_document(current_message, image_summary, table_text, llm)
    
    elif intent == 'summarize':
        response = summarize_document(image_summary, table_text, llm)

    return response