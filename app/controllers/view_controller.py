from app.services.blob_storage_service import get_file

def fetch_file_url(file_id, file_type, media_id):
    """
    Fetches a file url from the database.
    :param file_id: The ID of the file object.
    :return: A file url.
    """
    return get_file(file_id, file_type, media_id)


