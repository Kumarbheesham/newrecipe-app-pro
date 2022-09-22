from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse

class AdminTest(TestCase):
    """Set up to run before tests"""
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="bk@yopmail.com",
            password="Admin@123$"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="bkkhatri@yopmail.com",
            password="Admin@123",
            name="Test User full name"
        )

    def test_user_listed(self):
        """Test users are listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_edit_page(self):
        """Test user edit page"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_user_create_page(self):
        """Testing the user add page"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
