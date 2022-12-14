from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test user public api"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = {
            'email' : 'bkkhatri@yopmail.com',
            'password' : 'Admin@123',
            'name' : 'Jack'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Checking for already existing user"""
        payload = {
            'email' : "bkkhatri@yopmail.com",
            'password' : "Admin@123",
            'name' : 'Jack'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_password_too_short(self):
        """Checking if user password is too short"""
        payload = {
            'email' : 'bkkhatri@yopmail.com',
            'password' : 'Ad'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_token_is_created_for_user(self):
        """checking if user token is created"""
        payload = {
            'email' : 'bk@yopmail.com',
            'password' : 'Admin@123'
        }
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='bk@yopmail.com',password='Admin@123')
        payload = {'email' : 'bk@yopmail.com', 'password': 'notany'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token',res.data)

    def test_create_token_no_user(self):
        """Test that token not created if user doesn't exist"""
        payload = {'email': 'bk@yopmail.com', 'password':'Admin@123'}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_empty_fields(self):
        """Test that token not created if fields are empty"""
        res = self.client.post(TOKEN_URL, {'email':'one', 'password':""})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertTrue(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test api requests that requires authentications"""

    def setUp(self):
        self.user = create_user(
            email = "bk@yopmail.com",
            password = 'Admin@123',
            name = 'name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for loggedIn user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
        })

    def test_post_me_not_allowed(self):
        """Testing for post method not allowed"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Updating user profile"""
        payload= { 'email' : 'Jackpeterson@yopmail.com', 'password' : 'heyjack123', 'name': 'Jack'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

