

class MediaModel:
    def __init__(self, id, media_type, content_type, author, last_modified_date, location, description, tags, component_list, permissions, image_ids, video_ids, document_ids, text_search_vector, embedding_vector):
        self.id = id
        self.media_type = media_type
        self.content_type = content_type
        self.author = author
        self.last_modified_date = last_modified_date
        self.location = location
        self.description = description
        self.tags = tags
        self.component_list = component_list
        self.permissions = permissions
        self.image_ids = image_ids
        self.video_ids = video_ids
        self.document_ids = document_ids
        self.text_search_vector = text_search_vector
        self.embedding_vector = embedding_vector
