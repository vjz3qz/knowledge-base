import hashlib
from io import BytesIO
import json
import tempfile
from . import v1

from flask import Flask, request, jsonify, make_response
from flask_cors import CORS, cross_origin

import os
import sys

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings

from app.utils.determine_intent import determine_intent
from app.utils.document_processor import chunk_text, extract_text_from_stream, get_file_extension
from app.utils.query_document import query_document
from app.utils.summarize_document import summarize_document
from app.utils.report_pdf_generator import create_pdf
from app.utils.generate_unique_id import generate_unique_id, generate_image_hash
from app.utils.report_pdf_generator import create_pdf


# Ensure all required environment variables are set
try:
    os.environ['OPENAI_API_KEY']
except KeyError:
    print('[error]: `API_KEY` environment variable required')
    sys.exit(1)

from app.utils.document_retriever import upload_document_to_s3, upload_image_to_s3, get_metadata_from_s3, get_url_from_s3, extract_text_from_s3, call_lambda_function
from app.utils.vector_database_retriever import add_text_to_chroma, search_in_chroma, search_k_in_chroma

api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",
                 openai_api_key=api_key)


@v1.route('/upload', methods=['POST'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    pdf_buffer = BytesIO(pdf_file.read())
    text = extract_text_from_stream(pdf_buffer)
    chunked_text = chunk_text(text)
    # generate unique id with Document Level Hash
    file_id = generate_unique_id(text)
    # generate summary
    summary = summarize_document(chunked_text, llm)
    # add file to chroma
    add_text_to_chroma(chunked_text, file_id)
    # add file to S3 bucket
    pdf_file.seek(0)
    upload_document_to_s3(pdf_file, file_id, pdf_file.filename, summary)

    # Return the unique identifier to the frontend
    return jsonify({"id": file_id, "summary": summary, "filename": pdf_file.filename})

@v1.route('/upload-image', methods=['POST'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def upload_image():

    if 'file' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400
    image_file = request.files['file']
    if image_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    

    image_content = image_file.read()
    image_hash = generate_image_hash(image_content)
    image_file.seek(0)
    # upload to s3
    upload_image_to_s3(image_file, image_hash, image_file.filename, "trace-ai-images", "input-images")
    # # get s3 url
    # url = get_url_from_s3(image_hash, "trace-ai-images", "input-images")
    # get content type
    content_type, file_extension = get_file_extension(image_file.filename)
    # print(content_type)
    # call lambda function
    lambda_response = call_lambda_function(image_hash, content_type, file_extension)
    # get class counts for lambda function response
    # class_counts = lambda_response['class_counts']
    body_content = json.loads(lambda_response['body'])
    class_counts = body_content['class_counts']
    # print(lambda_response)
    # print(class_counts)

    # Return the unique identifier to the frontend

    return jsonify({"id": image_hash, "summary": json.dumps(class_counts), "filename": image_file.filename})
    # return jsonify({"id": image_hash,  "filename": image_file.filename})


@v1.route('/view/<file_id>', methods=['GET'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def view_file(file_id):
    url = get_url_from_s3(file_id)
    return jsonify(url=url)


@v1.route('/search-k', methods=['POST'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def search_k():
    query = request.json['query']
    if not request.json.get('k', None):
        k = 3
    else:
        k = int(request.json['k'])
    results = search_k_in_chroma(query, k)
    return jsonify(results)


@v1.route('/document-chat', methods=['POST'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def document_chat():
    current_message = request.json['current_message']
    conversation_history = request.json.get('conversation_history', [])
    pdf_id = request.json.get('id', None)

    # If no conversation history or PDF
    if not conversation_history and not pdf_id:
        response = "Error: No conversation history or PDF provided"

    # If there's both a PDF and conversation history
    elif pdf_id and conversation_history:
        intent = determine_intent(current_message)
        # TODO add logic for context awareness
        texts = extract_text_from_s3(pdf_id)
        chunks = chunk_text(texts)

        if intent == 'question':
            response = query_document(current_message, chunks, llm)

        elif intent == 'summarize':
            response = summarize_document(chunks, llm)

    # If there's only a PDF
    elif pdf_id and not conversation_history:
        intent = determine_intent(current_message)
        texts = extract_text_from_s3(pdf_id)
        chunks = chunk_text(texts)

        if intent == 'question':
            response = query_document(current_message, chunks, llm)

        elif intent == 'summarize':
            response = summarize_document(chunks, llm)

    else:
        response = {"error": "Unexpected scenario"}
    return jsonify({"response": response})



@v1.route('/metadata/<file_id>', methods=['GET'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def get_metadata(file_id):
    metadata = get_metadata_from_s3(file_id)
    return jsonify(metadata)





# ------------------ FUTURE ENDPOINTS ------------------


@v1.route('/search', methods=['POST'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def search():
    query = request.json['query']
    results = search_in_chroma(query)
    return jsonify(results)


@v1.route('/report', methods=['POST'])
@cross_origin(origins='*', allow_headers=['access-control-allow-origin', 'Content-Type'])
def report():
    type = request.json['reportType']
    name = request.json['name']
    employee_id = request.json['employeeId']
    role = request.json['role']
    date = request.json['date']

    data = {'Report Type': type,
            'Employee Name': name,
            'Employee ID': employee_id,
            'Role': role,
            'Date': date}

    if type == 'incident':
        data['Time of Incident'] = request.json['typeOfIncident']
        data['Incident Description'] = request.json['description']
        data['Incident Fix'] = request.json['fix']
        data['Incident Notes'] = request.json['notes']
    else:
        data['Work Location'] = request.json['workLocation']
        data['Work Description'] = request.json['workDescription']
        data['Work Problems'] = request.json['workProblems']
        data['Work Solutions'] = request.json['workSolutions']

    create_pdf(data)
    return make_response('', 201)


@v1.route('/upload-json', methods=['POST'])
@cross_origin(origins='*', allow_headers=['access-control-allow-origin', 'Content-Type'])
def upload_json():
    pdf_buffer, filename = create_pdf(request.json)

    text = extract_text_from_stream(pdf_buffer)
    chunked_text = chunk_text(text)
    # generate unique id with Document Level Hash
    file_id = generate_unique_id(text)
    # generate summary
    summary = summarize_document(chunked_text, llm)
    # add file to chroma
    add_text_to_chroma(chunked_text, file_id)
    # add file to S3 bucket
    pdf_buffer.seek(0)
    upload_document_to_s3(pdf_buffer, file_id, filename, summary)

    # Return the unique identifier to the frontend
    return jsonify({"id": file_id, "summary": summary, "filename": filename})
