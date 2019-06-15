from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """test creating user with email is successful"""
        email = 'test@gmail.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """test that new user is normalized"""
        email = "test@GMAIL.com"
        user = get_user_model()\
            .objects.create_user(email=email, password='test123')
        self.assertEqual(user.email, email.lower())
