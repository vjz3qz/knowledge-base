from pgvector.sqlalchemy import Vector
from database_service import db



class Component(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    hash = db.Column(db.String(64), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    location = db.Column(db.TEXT, nullable=False)
    media_list = db.Column(db.ARRAY(db.String))
    text_search_vector = db.Column(db.TSVECTOR)

    def __repr__(self):
        return f'<Media {self.id}>'

