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

@app.route('/upload', methods=['POST'])
@cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
def upload_file():
    pdf_file = request.files['file']
    page_selection = request.form['page_selection']
    page_number = int(request.form.get('page_number', 1))
    question = request.form.get('question', '')

    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_file.read())
        pdf_path = tmp_file.name
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()

        if page_selection == "Single page":
            view = pages[page_number - 1]
            texts = text_splitter.split_text(view.page_content)
            docs = [Document(page_content=t) for t in texts]
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            summaries = chain.run(docs)
            return jsonify({"summary": summaries})

        elif page_selection == "Overall Summary":
            combined_content = ''.join([p.page_content for p in pages])
            texts = text_splitter.split_text(combined_content)
            docs = [Document(page_content=t) for t in texts]
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            summaries = chain.run(docs)
            return jsonify({"summary": summaries})

        elif page_selection == "Question":
            combined_content = ''.join([p.page_content for p in pages])
            embedding = OpenAIEmbeddings()
            document_search = FAISS.from_texts(texts, embedding)
            chain = load_qa_chain(llm, chain_type="stuff")
            docs = document_search.similarity_search(question)
            summaries = chain.run(input_documents=docs, question=question)
            return jsonify({"summary": summaries})

    return jsonify({"error": "No PDF file uploaded"})

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')

# @cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
# def upload_file():
#     pdf_file = request.files['file']
#     page_selection = request.form['page_selection']
#     page_number = int(request.form.get('page_number', 1))
#     question = request.form.get('question', '')

#     with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
#         tmp_file.write(pdf_file.read())
#         pdf_path = tmp_file.name
#         loader = PyPDFLoader(pdf_path)
#         pages = loader.load_and_split()

#         if page_selection == "Single page":
#             view = pages[page_number - 1]
#             texts = text_splitter.split_text(view.page_content)
#             docs = [Document(page_content=t) for t in texts]
#             chain = load_summarize_chain(llm, chain_type="map_reduce")
#             summaries = chain.run(docs)
#             return jsonify({"summary": summaries})

#         elif page_selection == "Overall Summary":
#             combined_content = ''.join([p.page_content for p in pages])
#             texts = text_splitter.split_text(combined_content)
#             docs = [Document(page_content=t) for t in texts]
#             chain = load_summarize_chain(llm, chain_type="map_reduce")
#             summaries = chain.run(docs)
#             return jsonify({"summary": summaries})

#         elif page_selection == "Question":
#             combined_content = ''.join([p.page_content for p in pages])
#             embedding = OpenAIEmbeddings()
#             document_search = FAISS.from_texts(texts, embedding)
#             chain = load_qa_chain(llm, chain_type="stuff")
#             docs = document_search.similarity_search(question)
#             summaries = chain.run(input_documents=docs, question=question)
#             return jsonify({"summary": summaries})

#     return jsonify({"error": "No PDF file uploaded"})

# if __name__ == '__main__':
#     app.run(debug=True)
