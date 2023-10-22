# Streamlit library, used to create the user interface for the application.
import streamlit as st
from langchain.embeddings.openai import OpenAIEmbeddings
import tempfile
import time
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
import os

api_key = os.environ.get('OPENAI_API_KEY')

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo", openai_api_key=api_key)

# We need to split the text using Character Text Split such that it should not increase token size
text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
)

st.title("PDF Summarizer & QA")
pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

if pdf_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(pdf_file.read())
        pdf_path = tmp_file.name
        loader = PyPDFLoader(pdf_path)
        pages = loader.load_and_split()

        # User input for page selection
        page_selection = st.radio("Page selection", ["Single page", "Overall Summary", "Question"])

        run = st.button(label='Run')

        if page_selection == "Single page":
            page_number = st.number_input("Enter page number", min_value=1, max_value=len(pages), value=1, step=1)
            if run:
                view = pages[page_number - 1]
                texts = text_splitter.split_text(view.page_content)
                docs = [Document(page_content=t) for t in texts]
                chain = load_summarize_chain(llm, chain_type="map_reduce")
                summaries = chain.run(docs)
                st.subheader("Summary")
                st.write(summaries)

        elif run and page_selection == "Overall Summary":
            combined_content = ''.join([p.page_content for p in pages])  # we get entire page data
            texts = text_splitter.split_text(combined_content)
            docs = [Document(page_content=t) for t in texts]
            chain = load_summarize_chain(llm, chain_type="map_reduce")
            summaries = chain.run(docs)
            st.subheader("Summary")
            st.write(summaries)

        elif page_selection == "Question":
            question = st.text_input("Enter your question")
            if run:
                combined_content = ''.join([p.page_content for p in pages])
                texts = text_splitter.split_text(combined_content)
                embedding = OpenAIEmbeddings()
                document_search = FAISS.from_texts(texts, embedding)
                chain = load_qa_chain(llm, chain_type="stuff")
                docs = document_search.similarity_search(question)
                summaries = chain.run(input_documents=docs, question=question)
                st.write(summaries)

        else:
            time.sleep(30)
            st.warning("No PDF file uploaded")