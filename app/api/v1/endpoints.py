from . import v1

from flask import request, jsonify


@v1.route('/search-component', methods=['GET'])
def search_component():
    """
    Endpoint for searching for a component.

    Parameters:
    query (str): The search string.

    Returns:
    list: A list of component items that match the search criteria, including IDs, summaries, and other relevant metadata.
    """
    query = request.args.get('query', '')
    try:
        results = component_search(query)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(results)


@v1.route('/search-media', methods=['GET'])
def search_media():
    """
    Endpoint for searching the media/history associated with a component.

    Parameters:
    query (str): The search string.
    component_id (str): The ID of the component to search.

    Returns:
    list: A list of media items that match the search criteria, including IDs, summaries, and other relevant metadata.
    """
    query = request.args.get('query', '')
    component_id = request.args.get('component_id', '')
    try:
        results = combined_search_media(query, component_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(results)


@v1.route('/view-media', methods=['GET'])
def view_media():
    """
    Endpoint for viewing a media object.

    Parameters:
    media_id: media ID for the viewing session.

    Returns:
    JSON: A JSON object containing the description and the title of the media object.
    """
    media_id = request.args.get('media_id', '')
    try:
        viewing_session = fetch_media_object(media_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(viewing_session)
    

@v1.route('/create-component', methods=['POST'])
def create_component():
    """
    Endpoint for creating a new component item.

    Parameters:
    author (str): Author of the component.
    title (str): Title of the component.
    description (str): Actual content or summary.
    media_list (str): media associated with the component.

    Returns:
    JSON: A JSON object containing the confirmation of creation, including the hash of the new component item.
    """
    author = request.json['author']
    title = request.json['title']
    description = request.json['description']
    media_list = request.json['media_list']
    try:
        media_id = create_new_component(author, title, description, media_list)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(media_id)
    

@v1.route('/create-media', methods=['POST'])
def create_media():
    """
    Endpoint for creating a new media item.

    Parameters:
    author (str): Author of the media.
    title (str): Title of the media.
    description (str): Actual content or summary.
    component_id (str): Component associated with the media.

    TODO
    files (str): File data for images/videos/documents (to be stored in S3).

    Returns:
    JSON: A JSON object containing the confirmation of creation, including the ID of the new media item.
    """
    author = request.json['author']
    title = request.json['title']
    description = request.json['description']
    component_id = request.json['component_id']
    # files = request.json['files']
    try:
        media_id = create_new_media(author, title, description, component_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(media_id)

v1.route('/assistant-chat', methods=['POST'])
def assistant_chat():
    """
    Endpoint for chatting with the AI Assistant.

    Parameters:
    query (str): The user's message or question.

    Returns:
    JSON: A JSON object containing the chat message.
    """
    query = request.json['query']
    try:
        assistant_response = chat_with_assistant(query)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(assistant_response)



@v1.route('/test_db')
def test_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM media LIMIT 1;')  # Replace with your table name
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return str(data)
