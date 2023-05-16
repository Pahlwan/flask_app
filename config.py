import os
from dotenv import load_dotenv

load_dotenv("test.env")

class BaseConfig(object):
    MAIL_DEFAULT_SENDER = "noreply@flask.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ["EMAIL_USER"]
    MAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]
    JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
    JWT_ACCESS_TOKEN_EXPIRES = 3600
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "SqlAlchemy"
    SESSION_SQLALCHEMY_TABLE = "sessions"
    SECRET_KEY = os.environ["SECRET_KEY"]
    SECURITY_PASSWORD_SALT = os.environ["SECURITY_PASSWORD_SALT"]
    SECURITY_PASSWORD_HASH = "sha512_crypt"

    
class Config(BaseConfig):
    """Test config."""
    FLASK_DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    FRONTEND_URL = "http://localhost:3000"
    TESTING = True
    WTF_CSRF_ENABLED = False