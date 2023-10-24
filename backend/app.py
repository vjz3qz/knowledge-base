# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import tempfile
import uuid

import sys

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
text_splitter = CharacterTextSplitter(separator="\n", chunk_size=800, chunk_overlap=200, length_function=len)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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

    combined_content = extract_text(pdf_path)
    summary = summarize_document(combined_content)
    # summary = "Your summary will appear here"
    # Return the unique identifier to the frontend
    return jsonify({"id": file_id, "summary": summary, "filename": pdf_file.filename})


def determine_intent(message):
    # Check for question
    if message.endswith('?'):
        return 'question'
    
    # Check for common terms related to summarization
    summarization_terms = ['summarize', 'overview', 'brief me', 'tell me about']
    if any(term in message.lower() for term in summarization_terms):
        return 'summarize'
    
    # Default to question if no clear intent is determined
    return 'question'


@app.route('/chat_interact', methods=['POST'])
@cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
def chat_interact():
    current_message = request.json['current_message']
    conversation_history = request.json.get('conversation_history', [])
    pdf_id = request.json.get('id', None)

    # If no conversation history or PDF
    if not conversation_history and not pdf_id:
        # TODO
        # Your logic to get a response from the model based on the current message
        response = "Your logic to get a response based solely on the current message"

    # If there's both a PDF and conversation history
    elif pdf_id and conversation_history:
        pdf_path = file_mapping.get(pdf_id)
        intent = determine_intent(current_message)

        # Your logic to process the message based on the intent and the PDF
        # TODO add logic for context awareness
        combined_content = extract_text(pdf_path)

        if intent == 'question':
            # embedding = OpenAIEmbeddings()
            # texts = text_splitter.split_text(combined_content)
            # document_search = FAISS.from_texts(texts, embedding)
            # chain = load_qa_chain(llm, chain_type="stuff")
            # docs = document_search.similarity_search(current_message)
            # response = chain.run(input_documents=docs, question=current_message)
            response = query_document(current_message, combined_content)

        elif intent == 'summarize':
            response = summarize_document(combined_content)

    # If there's only a conversation
    elif conversation_history and not pdf_id:
        # TODO
        # Your logic to provide a context-aware response based on the conversation history
        response = "Your logic to get a context-aware response based on the conversation history"

    # If there's only a PDF
    elif pdf_id and not conversation_history:
        pdf_path = file_mapping.get(pdf_id)
        intent = determine_intent(current_message)

        # Similar to the logic above for just a PDF
        combined_content = extract_text(pdf_path)

        if intent == 'question':
            response = query_document(current_message, combined_content)

        elif intent == 'summarize':
            # texts = text_splitter.split_text(combined_content)
            # docs = [Document(page_content=t) for t in texts]
            # chain = load_summarize_chain(llm, chain_type="map_reduce")
            # response = chain.run(docs)
            response = summarize_document(combined_content)

    else:
        response = {"error": "Unexpected scenario"}

    return jsonify({"response": response})

def query_document(current_message, combined_content):
    embedding = OpenAIEmbeddings()
    texts = text_splitter.split_text(combined_content)
    document_search = FAISS.from_texts(texts, embedding)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = document_search.similarity_search(current_message)
    return chain.run(input_documents=docs, question=current_message)

def summarize_document(combined_content):
    texts = text_splitter.split_text(combined_content)
    docs = [Document(page_content=t) for t in texts]
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    return chain.run(docs)

def extract_text(pdf_path):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()
    combined_content = ''.join([p.page_content for p in pages])
    return combined_content





if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')