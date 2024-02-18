from flask import Flask
from flask_cors import CORS
from app.views.file_system import file_system_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.register_blueprint(file_system_blueprint, url_prefix='/api')

    return app
