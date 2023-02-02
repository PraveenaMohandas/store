from flask import Flask
from common.middleware import middleware
from settings.config.database import connect_to_db
from settings.register_blueprint import register_blueprint
import os

def create_app():
    app = Flask(__name__)
    app = connect_to_db(app)
    app = register_blueprint(app)
    middleware(app)
    SECRET_KEY = os.environ.get('SECRET_KEY')
       
    return app
