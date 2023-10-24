
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain



def query_document(current_message, texts, llm):
    embedding = OpenAIEmbeddings()
    document_search = FAISS.from_texts(texts, embedding)
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = document_search.similarity_search(current_message)
    return chain.run(input_documents=docs, question=current_message)