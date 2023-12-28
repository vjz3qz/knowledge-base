from . import v1

from flask import request, jsonify


@v1.route('/search', methods=['GET'])
def search():
    """
    Endpoint for searching the Chroma database.

    Parameters:
    query (str): The search string.
    mediaType (str): Filter by media type (note, document, diagram, video).
    contentType (str): Filter by content type.
    tags (str): Filter by tags (safety, maintenance, training, etc.).
    componentList (str): Filter by components listed in the media.

    Returns:
    list: A list of media items that match the search criteria, including IDs, summaries, and other relevant metadata.
    """
    query = request.args.get('query', '')
    media_type = request.args.get('mediaType', '')
    content_type = request.args.get('contentType', '')
    tags = request.args.get('tags', '')
    component_list = request.args.get('componentList', '')
    try:
        results = combined_search_media(query, media_type, content_type, tags, component_list)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(results)


@v1.route('/get-viewing-session', methods=['GET'])
def get_viewing_session():
    """
    Endpoint for getting a viewing session.

    Parameters:
    id (str): The unique identifier of the user.

    Returns:
    JSON: A JSON object containing the ID array of the user's viewing session.
    """
    id = request.args.get('id', '')
    try:
        viewing_session = get_viewing_session_by_id(id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify(viewing_session)

@v1.route('/add-viewing-session', methods=['POST'])
def add_viewing_session():
    """
    Endpoint for adding a viewing session.

    Parameters:
    userId (str): Identifier for the user.
    documentID (str): Document ID to add to the user's viewing session.

    Action:
    Saves the current state of the user's viewing session in the database.
    """
    user_id = request.json['userId']
    document_id = request.json['documentID']
    try:
        add_document_id_to_user_viewing_session(user_id, document_id)
    except Exception as e:
        # Optionally log the exception (not shown here)
        print(e)
        return jsonify({"error": "Server error"}), 500
    return jsonify({"success": True})



@v1.route('/create-media', methods=['POST'])
def create_media():
    """
    Endpoint for creating a new media item.

    Parameters:
    mediaType (str): Type of media being created (note, document, diagram, video).
    contentType (str): Content type of the media.
    author (str): Author of the media.
    description (str): Actual content or summary.
    tags (str): Tags associated with the media.
    componentList (str): Components associated with the media.
    permissions (str): Access permissions.
    files (str): File data for images/videos/documents (to be stored in S3).

    Returns:
    JSON: A JSON object containing the confirmation of creation, including the ID of the new media item.
    """
    media_type = request.json['mediaType']
    content_type = request.json['contentType']
    author = request.json['author']
    description = request.json['description']
    tags = request.json['tags']
    component_list = request.json['componentList']
    permissions = request.json['permissions']
    files = request.json['files']
    try:
        media_id = create_new_media(media_type, content_type, author, description, tags, component_list, permissions, files)
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
