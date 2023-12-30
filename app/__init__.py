from flask import Flask
from flask_cors import CORS
from app.api.v1 import v1 as v1_blueprint
import logging
from app.services.database_service import init_db


def create_app():
    app = Flask(__name__)
    CORS(app)  # if you're using Flask-CORS

    # Initialize the database
    init_db(app)

    # Configuration, blueprints registration, etc.
    logging.basicConfig(level=logging.DEBUG)
    # Registering the v1 blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    return app
