import unittest
from app.database.context import db
from app.auth.models import User
from app import create_app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_missing_username(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='', password='testpassword', firstname='Test', lastname='User', email='test@example.com', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'No username provided')

    def test_missing_password(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='', firstname='Test', lastname='User', email='test@example.com', phone='+91-1234567890')
                 
        self.assertEqual(exception_context.exception.args[0], 'No password provided')

    def test_missing_email(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='Test', lastname='User', email='', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'No email provided')

    def test_missing_firstname(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='', lastname='User', email='test@example.com', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'No firstname provided')

    def test_missing_lastname(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='Test', lastname='', email='test@example.com', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'No lastname provided')

    def test_missing_phone(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='Test', lastname='User', email='test@example.com', phone='')

        self.assertEqual(exception_context.exception.args[0], 'No phone provided')

    def test_invalid_email(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='Test', lastname='User', email='test', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'Invalid email address, must be in the format [email]@[domain]')

    def test_invalid_username(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='test', password='testpassword', firstname='Test', lastname='User', email='test@example.com' , phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'Username must be between 5 and 32 characters')   

    def test_invalid_password(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='test', firstname='Test', lastname='User', email='test@example.com', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'Password must be at least 8 characters')

    def test_invalid_firstname(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='T', lastname='User', email='test@example.com', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'Firstname must be between 2 and 32 characters')

    def test_invalid_lastname(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='Test', lastname='U', email='test@example.com', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'Lastname must be between 2 and 32 characters')

    def test_invalid_phone(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='Test', lastname='User', email='test@example.com', phone='1234567890')

        self.assertEqual(exception_context.exception.args[0], 'Invalid phone number, must be in the format +[country code]-[number]')

    def test_invalid_email_format(self):
        with self.assertRaises(AssertionError) as exception_context:
            User(username='testuser', password='testpassword', firstname='Test', lastname='User', email='test@example', phone='+91-1234567890')

        self.assertEqual(exception_context.exception.args[0], 'Invalid email address, must be in the format [email]@[domain]')


    def test_create_user(self):
        user = User(username='testuser', password='testpassword', firstname='Test', lastname='User', email="test@example.com", phone="+91-1234567890")
        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(username='testuser').first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, 'test@example.com')

    def test_delete_user(self):
        user = User(username='testuser', password='testpassword', firstname='Test', lastname='User', email="test@example.com", phone="+91-1234567890")
        db.session.add(user)
        db.session.commit()

        user_to_delete = User.query.filter_by(username='testuser').first()
        db.session.delete(user_to_delete)
        db.session.commit()

        deleted_user = User.query.filter_by(username='testuser').first()
        self.assertIsNone(deleted_user)

    def test_update_user(self):
        user = User(username='testuser', password='testpassword', firstname='Test', lastname='User', email="test@example.com", phone="+91-1234567890")
        db.session.add(user)
        db.session.commit()

        user_to_update = User.query.filter_by(username='testuser').first()
        user_to_update.username = 'updateduser'
        db.session.commit()

        updated_user = User.query.filter_by(username='updateduser').first()
        self.assertIsNotNone(updated_user)
        self.assertEqual(updated_user.username, 'updateduser')


if __name__ == '__main__':
    unittest.main()
