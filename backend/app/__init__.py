from flask import Flask, request, jsonify
from flask_cors import CORS
from app.api.v1 import v1 as v1_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)  # if you're using Flask-CORS

    # Configuration, blueprints registration, etc.

    # Registering the v1 blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    return app
