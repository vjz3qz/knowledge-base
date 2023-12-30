from pgvector.sqlalchemy import Vector
from database_service import db



class Media(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    hash = db.Column(db.String(64), unique=True, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    last_modified = db.Column(db.TIMESTAMP, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    component_ids = db.Column(db.ARRAY(db.TEXT))
    image_ids = db.Column(db.ARRAY(db.TEXT))
    video_ids = db.Column(db.ARRAY(db.TEXT))
    document_ids = db.Column(db.ARRAY(db.TEXT))
    text_search_vector = db.Column(db.TSVECTOR)
    embedding_vector = db.Column(Vector(1536))

    def __repr__(self):
        return f'<Media {self.id}>'

