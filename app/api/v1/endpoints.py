from . import v1

from flask import request, jsonify
# TODO support user creation and authentication

@v1.route('/search-component', methods=['GET'])
def search_component():
    """
    Endpoint for searching for a component.

    Parameters:
    query (str): The search string.

    Returns:
    list: A list of component records that match the search criteria.
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
    list: A list of media records that match the search criteria.
    """
    query = request.args.get('query', '')
    component_id = request.args.get('component_id', '')
    try:
        results = media_search(query, component_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(results)


@v1.route('/view-component', methods=['GET'])
def view_component():
    """
    Endpoint for viewing a component record.

    Parameters:
    component_id: component ID for the viewing session.

    Returns:
    JSON: A JSON object containing the description and the title of the component object.
    """
    component_id = request.args.get('component_id', '')
    try:
        component_record = fetch_component_record(component_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(component_record)


@v1.route('/view-media', methods=['GET'])
def view_media():
    """
    Endpoint for viewing a media record.

    Parameters:
    media_id: media ID for the viewing session.

    Returns:
    JSON: A JSON object containing the description and the title of the media object.
    """
    media_id = request.args.get('media_id', '')
    try:
        media_record = fetch_media_record(media_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(media_record)
    

@v1.route('/view-file', methods=['GET'])
def view_file():
    """
    Endpoint for viewing a file via url.

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
        file_url = fetch_file_url(file_id, file_type, media_id)
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
    title (str): Title of the component.
    description (str): Actual content or summary.
    location (str): Location of the component.

    Returns:
    JSON: A JSON object containing the confirmation of creation, including the id of the new component record.
    """
    title = request.json['title']
    description = request.json['description']
    location = request.json['location']
    try:
        component_id = create_new_component(title, description, location)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(component_id)
    

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
    JSON: A JSON object containing the confirmation of creation, including the ID of the new media record.
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
    file_data = request.json['file_data']
    file_type = request.json['file_type']
    media_id = request.json['media_id']
    try:
        file_id = add_new_file(file_data, file_type, media_id)
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