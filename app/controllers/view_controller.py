from app.services.database_service import get_component_by_id, get_media_by_id
from app.services.blob_storage_service import get_file


def fetch_component_record(component_id):
    """
    Fetches a component record from the database.
    :param component_id: The ID of the component object.
    :return: A component record.
    """
    return get_component_by_id(component_id)


def fetch_media_record(media_id):
    """
    Fetches a media record from the database.
    :param media_id: The ID of the media object.
    :return: A media record.
    """
    return get_media_by_id(media_id)
    

def fetch_file_url(file_id, file_type, media_id):
    """
    Fetches a file url from the database.
    :param file_id: The ID of the file object.
    :return: A file url.
    """
    return get_file(file_id, file_type, media_id)


