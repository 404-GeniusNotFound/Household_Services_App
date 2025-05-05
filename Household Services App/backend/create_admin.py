from app import create_app
from models import db, Admin
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    if not Admin.query.filter_by(email='admin@services.com').first():
        admin = Admin(
            email="admin@services.com",
            password=generate_password_hash("admin123", method='pbkdf2:sha256'),
            full_name="Admin User"
        )
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully.")
    else:
        print("Admin user already exists.")
