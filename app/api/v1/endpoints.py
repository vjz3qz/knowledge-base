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


@v1.route('/view-component', methods=['GET'])
def view_component():
    """
    Endpoint for viewing a component object.

    Parameters:
    component_id: component ID for the viewing session.

    Returns:
    JSON: A JSON object containing the description and the title of the component object.
    """
    component_id = request.args.get('component_id', '')
    try:
        viewing_session = fetch_component_object(component_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(viewing_session)


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
    

@v1.route('/view-file', methods=['GET'])
def view_file():
    """
    Endpoint for viewing a file object.

    Parameters:
    file_id: file ID for the viewing session.
    file_type (str): Type of file (image/video/document).
    media_id (str): Media associated with the file.

    Returns:
    JSON: A JSON object containing the url of the file object.
    """
    file_id = request.args.get('file_id', '')
    file_type = request.args.get('file_type', '')
    media_id = request.args.get('media_id', '')
    try:
        file_url = fetch_file_url(file_id, media_id, file_type)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(file_url)


@v1.route('/create-component', methods=['POST'])
def create_component():
    """
    Endpoint for creating a new component item.

    Parameters:
    author (str): Author of the component.
    title (str): Title of the component.
    description (str): Actual content or summary.
    location (str): Location of the component.
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
    component_ids (str): Component associated with the media.

    Returns:
    JSON: A JSON object containing the confirmation of creation, including the ID of the new media item.
    """
    author = request.json['author']
    title = request.json['title']
    description = request.json['description']
    component_ids = request.json['component_ids']
    try:
        media_id = create_new_media(author, title, description, component_ids)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(media_id)


@v1.route('/add-file', methods=['POST'])
def add_file():
    """
    Endpoint for adding a new file item.

    Parameters:
    file_type (str): Type of file (image/video/document).
    file_data (str): File data for images/videos/documents (to be stored in S3).
    media_id (str): Media associated with the file.

    Returns:
    JSON: A JSON object containing the confirmation of addition, including the ID of the new file item.
    """
    file_type = request.json['file_type']
    file_data = request.json['file_data']
    media_id = request.json['media_id']
    try:
        file_id = add_new_file(file_type, file_data, media_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(file_id)


@v1.route('/assistant-chat', methods=['POST'])
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
