from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Regexp
from models.Job import User
from sqlalchemy import or_

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=20, message='Username must be between 3 and 20 characters'),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Username can only contain letters, numbers, and underscores')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    role = SelectField('Role', choices=[
        ('user', 'Job Seeker'),
        ('admin', 'Employer')
    ], default='user')
    
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class LoginForm(FlaskForm):
    username_or_email = StringField('Username or Email', validators=[
        DataRequired(message='Username or email is required')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required')
    ])
    
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=2, max=50, message='Name must be between 2 and 50 characters')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    subject = StringField('Subject', validators=[
        DataRequired(message='Subject is required'),
        Length(min=5, max=100, message='Subject must be between 5 and 100 characters')
    ])
    
    message = TextAreaField('Message', validators=[
        DataRequired(message='Message is required'),
        Length(min=10, max=1000, message='Message must be between 10 and 1000 characters')
    ])
    
    submit = SubmitField('Send Message')

class JobForm(FlaskForm):
    company = StringField('Company', validators=[
        DataRequired(message='Company name is required'),
        Length(min=2, max=100, message='Company name must be between 2 and 100 characters')
    ])
    
    company_score = StringField('Company Score', validators=[
        DataRequired(message='Company score is required')
    ])
    
    job_title = StringField('Job Title', validators=[
        DataRequired(message='Job title is required'),
        Length(min=2, max=100, message='Job title must be between 2 and 100 characters')
    ])
    
    location = StringField('Location', validators=[
        DataRequired(message='Location is required'),
        Length(min=2, max=100, message='Location must be between 2 and 100 characters')
    ])
    
    salary = StringField('Salary', validators=[
        DataRequired(message='Salary is required')
    ])
    
    submit = SubmitField('Submit Job') 