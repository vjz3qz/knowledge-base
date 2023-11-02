import hashlib


def generate_unique_id(text):
    # Here, we're using a hash of the document content as its unique ID
    return hashlib.sha256(text.encode()).hexdigest()


def generate_image_hash(image_content):
    # Hash the image content
    return hashlib.sha256(image_content).hexdigest()
