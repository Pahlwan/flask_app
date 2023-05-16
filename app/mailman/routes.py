from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from app.auth.models import User
from app.mailman.utils import send_email

mailman_bp = Blueprint('mailman', __name__, url_prefix='/mailman', template_folder='templates')


@mailman_bp.route('/')
def index():
    return jsonify({'msg': 'Welcome to the email service'}), 200


@mailman_bp.route('/send', methods=['POST'])
@jwt_required()
def send():
    to = request.json.get('to')
    subject = request.json.get('subject')
    template_name = request.json.get('template_name')
    params = request.json.get('params')

    user = User.query.filter_by(email=to).first()

    if not user:
        return jsonify({'msg': 'User does not exist'}), 400

    send_email(to, subject, template_name, params)

    return jsonify({'msg': 'Email sent successfully'}), 200
