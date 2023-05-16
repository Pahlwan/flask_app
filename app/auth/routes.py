from flask import jsonify, request, current_app as app

from flask import Blueprint

from app.auth.models import User
from app.auth.utils import authenticate, create_token, verify_token
from app.mailman.utils import send_email

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')




@auth_bp.route('/login', methods=['POST'])
def login():
    username = request['username']
    password = request['password']

    if not username or not password:
        return jsonify({'msg': 'Missing username or password'}), 400

    user = authenticate(username, password)

    if not user:
        return jsonify({'msg': 'Invalid username or password'}), 401

    token = create_token(user)

    return jsonify({'access_token': token}), 200

@auth_bp.route('/register', methods=['POST'])
def register():
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    email = request.json.get('email')
    phone = request.json.get('phone')
    username = request.json.get('username')
    password = request.json.get('password')

    try:
        user  = User(username=username, firstname=firstname, lastname=lastname, email=email, phone=phone, password=password)
    except AssertionError as exception_message:
        return jsonify(msg=str(exception_message)), 400

    token = create_token(user, for_registration=True, expires_delta=3600)
    confirm_url = "{frontend_url}/confirm/email?token={token}".format(frontend_url=app.config['FRONTEND_URL'], token=token)
    if send_email(email, 'Confirm your email', 'confirm_email.html', confirm_url=confirm_url):
        user.save()
        return jsonify({'msg': 'Verification email sent'}), 201
    else:
        return jsonify({'msg': 'Error in sending verification email'}), 500
    

@auth_bp.route('/confirm/email', methods=['GET'])
def confirm_email():
    user = verify_token(request.args.get('token'))

    if not user:
        return jsonify({'msg': 'Invalid token'}), 401

    user.email_verified = True
    user.save()

    return jsonify({'msg': 'Email confirmed'}), 200
    