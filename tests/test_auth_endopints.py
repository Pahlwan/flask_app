import unittest
from flask_testing import TestCase
from app.database.context import db
from app.auth.models import User
from app.auth.utils import create_token
from app import create_app

class AuthTestCase(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '+91-7737713067'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 201)

        # Verify that the user was added to the database
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.firstname, 'Test')
        self.assertEqual(user.lastname, 'User')
        self.assertEqual(user.phone, '+91-7737713067')

    def test_verify_user_email(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@gmail.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '+91-7737713067'}
        response = self.client.post('/auth/register', json=data)

        user = User.query.filter_by(username='testuser').first()
        self.assertFalse(user.email_verified)

        token = create_token(user, True, 60)
        # headers = {'Authorization': 'Bearer ' + token}
        response = self.client.get('/auth/confirm/email', query_string={'token': token})
        self.assertEqual(response.status_code, 200)

        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(user.email_verified)


    def test_register_user_missing_username(self):
        data = {'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '1234567890'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'No username provided')

    def test_register_user_missing_password(self):
        data = {'username': 'testuser', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '+91-1234567890'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'No password provided')

    def test_register_user_missing_email(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'firstname': 'Test', 'lastname': 'User', 'phone': '1234567890'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'No email provided')

    def test_register_user_missing_firstname(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'lastname': 'User', 'phone': '1234567890'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'No firstname provided')

    def test_register_user_missing_lastname(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'phone': '1234567890'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'No lastname provided')

    def test_register_user_missing_phone(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'No phone provided')

    def test_register_user_duplicate_username(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '+91-7737713067'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 201)

        # Verify that the user was added to the database
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

        # Try to register the same user again
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'Username is already in use')

    def test_register_user_duplicate_email(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '+91-7737713067'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 201)

        # Verify that the user was added to the database
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

        # Try to register the same user again
        data['username'] = 'testuser2'
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'Email is already in use')

    def test_register_user_duplicate_phone(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '+91-7737713067'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 201)

        # Verify that the user was added to the database
        user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')

        # Try to register the same user again
        data['username'] = 'testuser2'
        data['email'] = 'test@example2.com'
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'Phone is already in use')

    def test_register_user_invalid_email(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test243', 'firstname': 'Test', 'lastname': 'User', 'phone': '+91-7737713067'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'Invalid email address, must be in the format [email]@[domain]')

    def test_register_user_invalid_phone(self):
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com', 'firstname': 'Test', 'lastname': 'User', 'phone': '1234567890'}
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)

        self.assertEqual(response.json['msg'], 'Invalid phone number, must be in the format +[country code]-[number]')
                
if __name__ == '__main__':
    unittest.main()
