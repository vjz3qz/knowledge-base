# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os

from langchain.chat_models import ChatOpenAI
import tempfile
import uuid
import sys

from app.utils.determine_intent import determine_intent
from app.utils.extract_text import extract_text
from app.utils.query_document import query_document
from app.utils.summarize_document import summarize_document

# Ensure all required environment variables are set
try:  
  os.environ['OPENAI_API_KEY']
except KeyError: 
  print('[error]: `API_KEY` environment variable required')
  sys.exit(1)


import logging
logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
# CORS(app, resources={r"/upload": {"origins": "http://localhost:3000"}})

CORS(app)

api_key = os.environ.get('OPENAI_API_KEY')
llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=api_key)


file_mapping = {}

@app.route('/upload', methods=['POST'])
@cross_origin(origin='*', headers=['access-control-allow-origin', 'Content-Type'])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    pdf_file = request.files['file']
    if pdf_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_file.read())
        pdf_path = tmp_file.name

    # Generate a unique identifier for the file
    file_id = str(uuid.uuid4())
    file_mapping[file_id] = pdf_path

    texts = extract_text(pdf_path)
    summary = summarize_document(texts, llm)

    # Return the unique identifier to the frontend
    return jsonify({"id": file_id, "summary": summary, "filename": pdf_file.filename})





@app.route('/chat_interact', methods=['POST'])
@cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
def chat_interact():
    current_message = request.json['current_message']
    conversation_history = request.json.get('conversation_history', [])
    pdf_id = request.json.get('id', None)

    # If no conversation history or PDF
    if not conversation_history and not pdf_id:
        response = "Error: No conversation history or PDF provided"

    # If there's both a PDF and conversation history
    elif pdf_id and conversation_history:
        pdf_path = file_mapping.get(pdf_id)
        intent = determine_intent(current_message)

        # Your logic to process the message based on the intent and the PDF
        # TODO add logic for context awareness
        texts = extract_text(pdf_path)

        if intent == 'question':
            response = query_document(current_message, texts, llm)

        elif intent == 'summarize':
            response = summarize_document(texts, llm)
    
    # If there's only a PDF
    elif pdf_id and not conversation_history:
        pdf_path = file_mapping.get(pdf_id)
        intent = determine_intent(current_message)

        # Similar to the logic above for just a PDF
        texts = extract_text(pdf_path)

        if intent == 'question':
            response = query_document(current_message, texts, llm)

        elif intent == 'summarize':
            response = summarize_document(texts, llm)

    else:
        response = {"error": "Unexpected scenario"}

    return jsonify({"response": response})





if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')