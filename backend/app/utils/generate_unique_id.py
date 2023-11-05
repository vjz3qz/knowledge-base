import hashlib


def generate_unique_id(content, file_type='text'):
    if file_type == 'text':
        # Here, we're using a hash of the document content as its unique ID
        return hashlib.sha256(content.encode()).hexdigest()
    elif file_type == 'image':
        return hashlib.sha256(content).hexdigest()
    elif file_type == 'binary':
        return hashlib.sha256(content).hexdigest()
    
def generate_image_hash(image_content):
    # Hash the image content
    return hashlib.sha256(image_content).hexdigest()

