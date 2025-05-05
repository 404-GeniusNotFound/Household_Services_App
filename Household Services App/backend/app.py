# app.py

from flask import Flask
from config_app import Config
from models import db
from flask_migrate import Migrate
from views.main import main_blueprint
from extensions import cache, mail, login_manager
from flask_cors import CORS
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        supports_credentials=True,
        resources={r"/*": {"origins": "http://localhost:8080"}},
        expose_headers='Authorization'
    )

    db.init_app(app)
    cache.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(main_blueprint)

    return app
