from app.services.database_service import search_components, search_media


def component_search(query):
    """
    Keyword searches database for matching text

    Parameters:
    -----------
    query : string
        user query

    Returns:
    --------
    List[Documents]
        Matched docs based on user query
    """
    return search_components(query)


def media_search(query, component_id):
    """
    Keyword searches database for matching text

    Parameters:
    -----------
    query : string
        user query

    Returns:
    --------
    List[Documents]
        Matched docs based on user query
    """
    return search_media(query, component_id)
