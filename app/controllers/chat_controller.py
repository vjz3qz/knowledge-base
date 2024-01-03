
import os

def chat_with_assistant(query):
    embedding = generate_embedding(query)
    search_results = similarity_search(embedding)
    response = llm_inference(query, search_results)
    return response


