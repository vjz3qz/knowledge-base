# Trace AI Flask Server Logic


TODO
create seed.sql and configure migrations
finish search methods in database_service.py



component_media_association = db.Table('component_media_association',
    db.Column('media_id', db.BIGINT, db.ForeignKey('media.id'), primary_key=True),
    db.Column('component_id', db.BIGINT, db.ForeignKey('component.id'), primary_key=True)
)

class Component(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    location = db.Column(db.TEXT, nullable=False)    
    text_search_vector = db.Column(db.TSVECTOR)

class Media(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.TIMESTAMP, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.TEXT, nullable=False)
    image_ids = db.Column(db.ARRAY(db.TEXT))
    video_ids = db.Column(db.ARRAY(db.TEXT))
    document_ids = db.Column(db.ARRAY(db.TEXT))
    text_search_vector = db.Column(db.TSVECTOR)

class User(db.Model):
    id = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)