from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')
VALID_USER_PAYLOAD = {
            'email': 'test1@gmail.com',
            'password': 'password',
            'name': 'tony'
        }


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test users API"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_successfull(self):
        """Test user with valid payload is created"""
        res = self.client.post(CREATE_USER_URL, VALID_USER_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(VALID_USER_PAYLOAD['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creating existing user fails"""
        create_user(**VALID_USER_PAYLOAD)
        res = self.client.post(CREATE_USER_URL, VALID_USER_PAYLOAD)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test passowrd must be more than 5 characters"""
        payload = {
            'email': 'test1@gmail.com',
            'password': 'pass',
            'name': 'tony'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload['email'])\
            .exists()
        self.assertFalse(user_exists)

    def test_create_user_token(self):
        """Test token is created for user"""
        create_user(**VALID_USER_PAYLOAD)
        res = self.client.post(TOKEN_URL, VALID_USER_PAYLOAD)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_with_invalid_credentials(self):
        """test token is not created for invalid credentials"""
        wrong_payload = \
            {'email': 'test1@gmail.com', 'password': 'wrongpassword'}
        create_user(**VALID_USER_PAYLOAD)
        res = self.client.post(TOKEN_URL, wrong_payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """test that token is not created if user dosent exist"""
        res = self.client.post(TOKEN_URL, VALID_USER_PAYLOAD)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """test that email and password are required"""
        payload = {'email': 'test1@gmail.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """Test user API requests with authentication"""
    def setUp(self):
        self.user = create_user(**VALID_USER_PAYLOAD)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """test retrieving details of authenticated user"""

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_not_allowed(self):
        """Test that post not allowed on me endpopint"""
        res = self.client.post(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile"""
        payload = {
            "name": "new name", "password": "new password"
        }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
