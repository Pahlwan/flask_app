from flask_jwt_extended import create_access_token
from flask import current_app as app
import jwt
from datetime import timedelta

from app.auth.models import User

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user

def create_token(user, for_registration, expires_delta=False):
    if for_registration:
        token = create_access_token(identity=user.email, expires_delta=timedelta(seconds=expires_delta))
    else:
        token = create_access_token(identity=user.id)
    return token

def verify_token(token):
    try:
        email = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])['sub']
        user = User.query.filter_by(email=email).first()
        return user
    except Exception as e:
        return None

    

