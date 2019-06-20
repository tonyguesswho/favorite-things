from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@gmail.com', password='password'):
    """Creare a sample user"""

    return get_user_model().objects.create_user(email, password)


def sample_category():
    """Creare a sample category"""

    return models.Category.objects.create(name='Rivers')


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

    def test_new_user_invalid_email(self):
        """Test invalid email error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testp')

    def test_create_superuser(self):
        """Test create new super user is successful"""

        user = get_user_model().objects.create_superuser(
            'super@gmail.com', 'pass'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_category_str(self):
        """Test create category string representation"""

        category = models.Category.objects.create(name='Rivers')
        self.assertEqual(str(category), category.name)

    def test_favorite_str(self):
        """Test create category string representation"""

        favorite_thing = models.Favorite.objects.create(
            title='Nile',
            user=sample_user(),
            description="The river nile is really big",
            ranking=1,
            category=sample_category())
        self.assertEqual(str(favorite_thing), favorite_thing.title)
