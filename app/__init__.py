from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from config import Config

from app.database.context import db


mail = Mail()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)
    CORS(app)

    # Initialize extensions
    mail.init_app(app)
    jwt.init_app(app)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.mailman import mailman_bp
    app.register_blueprint(mailman_bp)


    return app
