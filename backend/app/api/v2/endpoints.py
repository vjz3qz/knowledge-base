from . import v2

from flask import request, jsonify
from flask_cors import cross_origin

import os
import sys

from langchain.chat_models import ChatOpenAI

from app.utils.determine_intent import determine_intent
from app.utils.document_processor import chunk_text
from app.utils.query_document import query_document
from app.utils.summarize_document import summarize_document

from app.utils.document_retriever import upload_document_to_s3, upload_image_to_s3, get_metadata_from_s3, get_url_from_s3, extract_text_from_s3, extract_image_summary_from_s3, extract_table_text_from_s3




try:
    os.environ['OPENAI_API_KEY']
except KeyError:
    print('[error]: `API_KEY` environment variable required')
    sys.exit(1)


api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",
                 openai_api_key=api_key)






@v1.route('/upload', methods=['POST'])
@cross_origin()
def upload():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    text_file = request.files['file']
    if text_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    content_type = request.json['content_type']
    file_type = request.json['file_type']
    if file_type not in ['text', 'diagram']:
        return jsonify({"error": "Invalid file type"}), 400
    elif file_type == 'text':
        # Checks if it is txt, pdf, or docx, calls appropriate handler
        # if not appropriate handler, return error
        if content_type not in ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            return jsonify({"error": "Invalid content type"}), 400
        elif content_type == 'text/plain':
            txt_file_handler(text_file)
        elif content_type == 'application/pdf':
            pdf_file_handler(text_file)
        elif content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            docx_file_handler(text_file)
        
        # for each file type:
        # generate unique id with Document Level Hash
        # generate summary
        # add file to chroma
        # add file to S3 bucket: trace-ai-documents

    elif file_type == 'diagram':
        # Checks if it is pdf, jpeg/jpg, or png, calls appropriate handler. if not appropriate handler, return error
        if content_type not in ['application/pdf', 'image/jpeg', 'image/png']:
            return jsonify({"error": "Invalid content type"}), 400
        elif content_type == 'application/pdf':
            pdf_file_handler(diagram_file)
        elif content_type == 'application/jpeg':
            jpeg_file_handler(diagram_file)
        elif content_type == 'application/png':
            png_file_handler(diagram_file)
        
        # for each file type:
        # generate unique id with Document Level Hash
        # generate summary: call lambda function to get class counts, bounding boxes, and confidence scores
        # create descriptive text representation of diagram: based on class counts, bounding boxes, and confidence scores
        # add text representation to chroma
        # add file to S3 bucket: trace-ai-documents

    return "Success", 200


@app.route('/view/<file_id>', methods=['GET'])
@cross_origin()  
def view_file(file_id):
    if not file_id:
        return jsonify({"error": "No file id specified"}), 400
    
    # Assume file_id should be a non-empty string
    if not isinstance(file_id, str) or not file_id:
        return jsonify({"error": "Invalid file id"}), 400
    
    try:
        url = get_url_from_s3(file_id)
    except Exception as e:
        # Log the exception (not shown here)
        return jsonify({"error": "Server error"}), 500
    
    return jsonify(url=url)


@v1.route('/search/<k>', methods=['POST'])
@cross_origin()
def search_k(k):
    if not k:
        return jsonify({"error": "No k specified"}), 400

    # Ensure request.json is not None and contains 'query'
    if not request.json or 'query' not in request.json:
        return jsonify({"error": "No query provided"}), 400

    query = request.json['query']

    try:
        results = search_k_in_chroma(query, k)
    except Exception as e:
        # Optionally log the exception (not shown here)
        return jsonify({"error": "Server error"}), 500

    return jsonify(results)


@v1.route('/document-chat', methods=['POST'])
@cross_origin()
def document_chat():
    current_message = request.json['current_message']
    conversation_history = request.json.get('conversation_history', [])
    file_id = request.json.get('id', None)
    file_type = request.json.get('file_type', None)
    
    # If no conversation history or file
    if not conversation_history and not file_id:
        response = {"Error": "No conversation history or file provided"}

    # TODO add logic for context awareness


    # RAG using multimodal llm:
    # check if it is text or a diagram

    intent = determine_intent(current_message)

    # if text, extract text from file
    if file_id and file_type == 'text':
        
        texts = extract_text_from_s3(file_id)
        chunks = chunk_text(texts)

        if intent == 'question':
            response = query_document(current_message, chunks, llm)

        elif intent == 'summarize':
            response = summarize_document(chunks, llm)

    # if diagram, pass image summary and table text representation to llm
    elif file_id and file_type == 'diagram':
        # diagram
        image_summary = extract_image_summary_from_s3(file_id)
        table_text = extract_table_text_from_s3(file_id)

        if intent == 'question':
            response = query_document(current_message, image_summary, table_text, llm)
        
        elif intent == 'summarize':
            response = summarize_document(image_summary, table_text, llm)
    else:
        response = {"error": "Unexpected scenario"}
    return jsonify({"response": response})

