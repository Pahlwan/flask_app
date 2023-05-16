from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
import re

from app.database.context import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(32), unique=True, nullable=False)
    email_verified = db.Column(db.Boolean, default=False)
    phone_verified = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided')

        if User.query.filter(User.username == username).first():
            raise AssertionError('Username is already in use')

        if len(username) < 5 or len(username) > 32:
            raise AssertionError('Username must be between 5 and 32 characters')

        return username
    
    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise AssertionError('No password provided')

        if len(password) < 8:
            raise AssertionError('Password must be at least 8 characters')

        return generate_password_hash(password)
    
    @validates('firstname')
    def validate_firstname(self, key, firstname):
        if not firstname:
            raise AssertionError('No firstname provided')

        if len(firstname) < 2 or len(firstname) > 32:
            raise AssertionError('Firstname must be between 2 and 32 characters')

        return firstname
    
    @validates('lastname')
    def validate_lastname(self, key, lastname):
        if not lastname:
            raise AssertionError('No lastname provided')

        if len(lastname) < 2 or len(lastname) > 32:
            raise AssertionError('Lastname must be between 2 and 32 characters')

        return lastname
    
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')

        if User.query.filter(User.email == email).first():
            raise AssertionError('Email is already in use')
        
        EMAIL_REGEX = r'^[\w+\-.]+@[a-z\d\-]+(\.[a-z]+)*\.[a-z]+$'
        if not re.match(EMAIL_REGEX, email):
            raise AssertionError('Invalid email address, must be in the format [email]@[domain]')
        
        return email
    
    @validates('phone')
    def validate_phone(self, key, phone):
        if not phone:
            raise AssertionError('No phone provided')

        if User.query.filter(User.phone == phone).first():
            raise AssertionError('Phone is already in use')
        
        PHONE_REGEX = r'^\+[1-9]{1,3}-\d{1,14}$'
        if not re.match(PHONE_REGEX, phone):
            raise AssertionError('Invalid phone number, must be in the format +[country code]-[number]')

        return phone

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.username
    