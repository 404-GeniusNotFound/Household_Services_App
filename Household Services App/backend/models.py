from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz
from babel.numbers import format_currency

db = SQLAlchemy()

IST = pytz.timezone('Asia/Kolkata')

def format_date_to_ist(date):
    if date:
        return date.astimezone(IST).strftime('%d-%m-%Y %I:%M %p')
    return None

def format_price(price):
    return format_currency(price, 'INR', locale='en_IN') if price is not None else None

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)

    def get_id(self):
        return f"admin-{self.id}"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email
        }

class Customer(UserMixin, db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)

    def get_id(self):
        return f"customer-{self.id}"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "pin_code": self.pin_code
        }

class Professional(UserMixin, db.Model):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)
    service_name = db.Column(db.String(100), nullable=True)
    experience = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), nullable=True)
    cv_file = db.Column(db.String(255), nullable=True)

    def get_id(self):
        return f"professional-{self.id}"

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone_number": self.phone_number,
            "address": self.address,
            "pin_code": self.pin_code,
            "service_name": self.service_name,
            "experience": self.experience,
            "status": self.status,
            "cv_file": self.cv_file
        }

class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=False)

    service_requests = db.relationship('ServiceRequest', backref='related_service')

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": format_price(self.price),
            "description": self.description,
            "category": self.category,
        }

class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=True)
    status = db.Column(db.String(20), default='requested')
    remarks = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=True)
    request_date = db.Column(db.DateTime, nullable=True)
    completion_date = db.Column(db.DateTime, nullable=True)

    customer = db.relationship('Customer', backref='customer_requests')
    professional = db.relationship('Professional', backref='professional_requests', foreign_keys=[professional_id])

    def to_dict(self):
        return {
            "id": self.id,
            "service_id": self.service_id,
            "service_name": self.related_service.name if self.related_service else None,
            "customer_id": self.customer_id,
            "customer_name": self.customer.full_name if self.customer else None,
            "customer_phone": self.customer.phone_number if self.customer else None,
            "customer_location": f"{self.customer.address}, {self.customer.pin_code}" if self.customer else None,
            "professional_id": self.professional_id,
            "professional_name": self.professional.full_name if self.professional else None,
            "professional_phone": self.professional.phone_number if self.professional else None,
            "status": self.status,
            "remarks": self.remarks,
            "rating": self.rating,
            "request_date": format_date_to_ist(self.request_date) if self.request_date else None,
            "completion_date": format_date_to_ist(self.completion_date) if self.completion_date else None
        }
