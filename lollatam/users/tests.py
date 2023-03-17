from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.forms import UserForm
from users.models import Profile, User

class SignupViewTest(TestCase):
    def setUp(self):
        self.signup_url = reverse('users:signup')
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        self.existing_username_user_data = {
            'username': 'testuser1',
            'first_name': 'Existing',
            'last_name': 'User',
            'email': 'testuser1@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        self.existing_email_user_data = {
            'username': 'testuser2',
            'first_name': 'Existing',
            'last_name': 'User',
            'email': 'testuser2@example.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        self.existing_username_user = get_user_model().objects.create_user(
            username='testuser1',
            email='testuser11@example.com',
            password='testpass123',
        )
        self.existing_email_user = get_user_model().objects.create_user(
            username='testuser22',
            email='testuser2@example.com',
            password='testpass123',
        )
        Profile.objects.create(user=self.existing_username_user)
        Profile.objects.create(user=self.existing_email_user)


    def test_signup_form_valid(self):
        # Test that a valid form submission creates a new user and logs them in
        response = self.client.post(self.signup_url, data=self.user_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('network:profile'))
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())

    def test_signup_form_invalid(self):
        # Test that an invalid form submission does not create a new user
        response = self.client.post(self.signup_url, data={'username': 'testuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertFalse(get_user_model().objects.filter(username='testuser').exists())

    def test_already_authenticated(self):
        # Test that an authenticated user is redirected to their profile
        self.client.login(username='testuser1', password='testpass123')
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('network:profile'))
