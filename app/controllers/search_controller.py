from app.services.database_service import execute_query
from app.services.openai_service import generate_embedding
from app.models.media_model import MediaModel

def combined_search_media(query, media_type, content_type, tags, component_list):
    # Step 1: Perform Full-Text Search
    full_text_results = full_text_search(query, media_type, content_type, tags, component_list)

    # Step 2: Perform Semantic Search
    semantic_search_results = semantic_search(query, media_type, content_type, tags, component_list)

    # Step 3: Combine and Process Results
    combined_results = combine_and_process_results(full_text_results, semantic_search_results)

    return combined_results

def full_text_search(query, media_type, content_type, tags, component_list):
    # Construct the full-text search query
    # Note: Use parameterized queries to prevent SQL injection
    full_text_query = "SELECT * FROM your_media_table WHERE textsearchable_index_col @@ plainto_tsquery(%s)"
    params = [query]

    # Add additional filters based on provided parameters
    # ...

    # Execute the query using the database service
    rows = execute_query(full_text_query, params)
    return [MediaModel.from_row(row) for row in rows]

def semantic_search(query, media_type, content_type, tags, component_list):
    # Generate embedding for the query using OpenAI API
    query_embedding = generate_embedding(query)

    # Construct the semantic search query
    # Note: The specifics depend on your vector extension
    semantic_query = "SELECT * FROM your_media_table WHERE your_vector_similarity_function(embedding_vector, %s) > threshold"
    params = [query_embedding]

    # Add additional filters based on provided parameters
    # ...

    # Execute the query using the database service
    rows = execute_query(semantic_query, params)
    return [MediaModel.from_row(row) for row in rows]

def combine_and_process_results(full_text_results, semantic_search_results):
    # Combine, deduplicate, and sort the results
    # This function should be tailored based on your specific requirements
    # ...

    combined_results = full_text_results + semantic_search_results  # Simplistic approach
    return combined_results
