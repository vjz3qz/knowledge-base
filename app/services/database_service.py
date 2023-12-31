# database_service.py
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

media_component_association = db.Table('media_component_association',
    db.Column('media_id', db.BIGINT, db.ForeignKey('media.id'), primary_key=True),
    db.Column('component_id', db.BIGINT, db.ForeignKey('component.id'), primary_key=True)
)

def init_db(app):
    """Initialize the database with the given Flask app."""
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

