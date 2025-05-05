import os
from dotenv import load_dotenv
from flask_login import LoginManager

load_dotenv()

class Config:
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', 'default-salt')

    # Database path
    DB_PATH = os.getenv('DB_PATH', 'I:/MAD2 Project/db/app.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'

    # Celery settings
    BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
    RESULT_BACKEND = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')
    BROKER_CONNECTION_RETRY_ON_STARTUP = True

    # Email settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    # Cache settings
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL', 'redis://localhost:6379/1')

# Initialize login_manager
login_manager = LoginManager()
