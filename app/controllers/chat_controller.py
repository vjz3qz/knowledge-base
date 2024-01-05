from app.services.ai_text_service import llm_inference
from app.services.database_service import similarity_search


def chat_with_assistant(query):
    search_results = similarity_search(query)
    response = llm_inference(query, search_results)
    return response
