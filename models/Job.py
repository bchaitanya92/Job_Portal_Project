from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
import re
from datetime import datetime
from flask_login import UserMixin

class JobPortal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    company_score = db.Column(db.Integer, nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # New: link to User
    provider = db.relationship('User', backref='posted_jobs')  # New: relationship

    @validates('company_score')
    def validate_company_score(self, key, value):
        if value < 0 or value > 5:
            raise ValueError("Company score must be between 0 and 5.")
        return value
    
    # def __init__(self, company, company_score, job_title, location, date, salary):
    #     self.company = company
    #     self.company_score = company_score
    #     self.job_title = job_title
    #     self.location = location
    #     self.date = date
    #     self.salary = salary

    def to_dict(self):
        return {
            'id': self.id,
            'company': self.company,
            'company_score': self.company_score,
            'job_title': self.job_title,
            'location': self.location,
            'date': self.date.strftime('%Y-%m-%d'),
            'salary': self.salary,
        }


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, username, email, password, role='user'):
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    def get_id(self):
        return str(self.id)

    @validates('email')
    def validate_email(self, key, email):
        # Basic email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email

    @validates('username')
    def validate_username(self, key, username):
        # Username validation: 3-20 characters, alphanumeric
        if not re.match(r"^[a-zA-Z0-9_]{3,20}$", username):
            raise ValueError("Username must be 3-20 characters long and contain only letters, numbers, and underscores")
        return username
    
# Add this model to your models.py
class FailedLoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<FailedLoginAttempt {self.user_id} {self.timestamp}>'

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job_portal.id'), nullable=False)
    seeker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    resume_link = db.Column(db.String(256), nullable=True)

    job = db.relationship('JobPortal', backref='applications')
    seeker = db.relationship('User', backref='applications')

    def __repr__(self):
        return f'<Application job_id={self.job_id} seeker_id={self.seeker_id}>'