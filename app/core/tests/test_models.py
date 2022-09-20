from django.test import TestCase;
from django.contrib.auth import get_user_model;

class ModelTests(TestCase):

    """test creating a new user with an email and password"""
    def test_create_user_with_email_successfull(self):
        email="bkkhatri@yopmail.com"
        password="Admin@123$"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(email,user.email)
        self.assertTrue(user.check_password(password))

    """testing the user email normalized"""
    def test_create_user_with_normalized_email(self):
        email="bkkhatri@YOPMAIL.COM"
        """password already tested so just passing string"""
        user = get_user_model().objects.create_user(
            email,'Admin@123$'
        )

        self.assertEqual(email.lower(), user.email)

    """Testing for if email is provided else raise error"""
    def test_email_invalid_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Admin@123')

    """Testing for creating super user"""
    def test_is_superuser(self):
        user = get_user_model().objects.create_superuser(
            "bk123@yopmail.com",
            'Admin@123$'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)