# extensions.py

from flask_caching import Cache
from flask_mail import Mail
from flask_login import LoginManager

# Initialize Flask extensions
cache = Cache()
mail = Mail()
login_manager = LoginManager()
