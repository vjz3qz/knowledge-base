import hashlib


def generate_unique_id(text):
    # Here, we're using a hash of the document content as its unique ID
    return hashlib.sha256(text.encode()).hexdigest()