from . import v2

from flask import request, jsonify
from flask_cors import cross_origin

import os
import sys

from langchain.chat_models import ChatOpenAI

from app.utils.determine_intent import determine_intent
from app.utils.document_retriever import get_url_from_s3
from app.controllers.upload_controller import upload_file_handler

from app.utils.vector_database_retriever import search_k_in_chroma


try:
    os.environ['OPENAI_API_KEY']
except KeyError:
    print('[error]: `API_KEY` environment variable required')
    sys.exit(1)


api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k",
                 openai_api_key=api_key)



@v2.route('/upload', methods=['POST'])
@cross_origin()
def upload():

    """
    Endpoint for uploading a document.

    Request Body:
    content_type (str): The content type of the file.
    file (file): The file to be uploaded.
    file_type (str): The type of the file (text or diagram).
    
    The function checks if the file is text or diagram based on the content type.
    It also checks the file format and calls the appropriate handler.

    Returns:
    str: A string indicating the status code of the operation.
    """

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    content_type = request.form['content_type']
    file_type = request.form['file_type']

    if file_type not in ['text', 'diagram']:
        return jsonify({"error": "Invalid file type"}), 400

    # if not appropriate handler, return error
    if content_type not in ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'image/jpeg', 'image/png']:
        return jsonify({"error": "Invalid content type"}), 400
    
    upload_file_handler(uploaded_file, llm, content_type, file_type)
        
    return "Success", 200


@v2.route('/view/<file_id>', methods=['GET'])
@cross_origin()  
def view_file(file_id):
    """
    Endpoint to retrieve the URL of a document stored in S3.

    Parameters:
    file_id (str): The unique identifier of the document.

    Returns:
    JSON: A JSON object containing the URL of the document in S3.
    """
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


@v2.route('/search/<k>', methods=['POST'])
@cross_origin()
def search_k(k):
    """
    Endpoint for searching the knowledge base.

    Parameters:
    k (int): The number of sources to retrieve.

    Request Body:
    natural_language_query (str): The query in natural language.

    Returns:
    JSON: A JSON object containing a list of sources, each with an S3 URL and metadata.
    """
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


@v2.route('/document-chat', methods=['POST'])
@cross_origin()
def document_chat():
    """
    Endpoint for chatting about a document.

    Request Body:
    user_message (str): The user's message.
    conversation_history (list): The conversation history.
    id (str): The unique identifier of the document.
    file_type (str): The type of the file (text or diagram).

    Returns:
    JSON: A JSON object containing the chat message.
    """
    user_message = request.json['user_message']
    conversation_history = request.json.get('conversation_history', [])
    file_id = request.json.get('id', None)
    file_type = request.json.get('file_type', None)
    # If no conversation history or file
    if not conversation_history and not file_id:
        response = {"Error": "No conversation history or file provided"}
    # TODO add logic for context awareness
    # RAG using multimodal llm:
    # check if it is text or a diagram
    intent = determine_intent(user_message)
    response = rag_handler(user_message, file_id, intent, llm, file_type)
    # if text, extract text from file
    # if diagram, pass image summary and table text representation to llm

    return jsonify({"response": response})