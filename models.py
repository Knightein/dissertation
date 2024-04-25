import sqlite3

import bcrypt

from flask import render_template
from flask_login import UserMixin, current_user
from datetime import datetime
from cryptography.fernet import Fernet
from functools import wraps
from app import app, db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)

    # Auth
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)

    # Info
    firstname = db.Column(db.String(40), nullable=False)
    lastname = db.Column(db.String(40), nullable=False)
    role = db.Column(db.String(30), nullable=False, default='student')
    registered_on = db.Column(db.DateTime, nullable=False)
    current_login = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)

    # Encryption
    postkey = db.Column(db.BLOB, nullable=False)

    def __init__(self, email, firstname, lastname, password, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname

        # Encrypt the password
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        self.role = role
        self.registered_on = datetime.now()

        # Set to None, as the user has not logged in yet, there is no information to add
        self.current_login = None
        self.last_login = None

        # Generate a random key to set as the user's encryption key
        self.postkey = Fernet.generate_key()


class Assignment(db.Model):
    __tablename__ = 'assignments'
    __table_args__ = {'extend_existing': True}

    assignment_id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    set_by = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)

    # String is 10 for yyyy-mm-dd format (will use regex)
    due_date = db.Column(db.String(10), nullable=False)

    def __init__(self, name, description, set_by, due_date):
        self.name = name
        self.description = description
        self.set_by = set_by
        self.created_on = datetime.now()
        self.due_date = due_date


class Grade(db.Model):
    __tablename__ = 'grades'
    __table_args__ = {'extend_existing': True}

    assignment_id = db.Column(db.Integer, db.ForeignKey(Assignment.assignment_id), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    grade = db.Column(db.String(1), nullable=True, default='N')
    correct = db.Column(db.Boolean, nullable=False, default=False)
    feedback = db.Column(db.String(2000), nullable=False, default='No Feedback Provided. Default.')
    next_steps = db.Column(db.String(2000), nullable=False, default='No Next Steps Provided. Default.')
    code_submission = db.Column(db.String(2000), nullable=False, default='No Code Provided. Default.')
    grade_id = db.Column(db.Integer, primary_key=True)

    def __init__(self, assignment_id, student_id, grade, correct, feedback, next_steps, code_submission):
        self.assignment_id = assignment_id
        self.student_id = student_id
        self.grade = grade
        self.correct = correct
        self.feedback = feedback
        self.next_steps = next_steps
        self.code_submission = code_submission


# Do not use this function as it will delete all data in the database
def init_db():
    print("Initializing Database!")
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(email='admin@email.com',
                     firstname='Admin',
                     lastname='Admin',
                     password='Admin1!',
                     role='teacher')

        db.session.add(admin)
        db.session.commit()
        print("Database Initialized!")


# Encrypt Function
def encrypt(data, postkey):
    # Encrypts the data provided through the parameter with the User's Encryption Key
    return Fernet(postkey).encrypt(bytes(data.encode('utf-8')))


# Decrypt Function
def decrypt(data, postkey):
    # Decrypts the data provided through the parameter with the User's Encryption Key
    return Fernet(postkey).decrypt(data).decode('utf-8')


# RBAC
def required_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Check if the role exists
            if current_user.role not in roles:
                return render_template('error/403.html')
            return f(*args, **kwargs)
        return wrapped
    return wrapper
