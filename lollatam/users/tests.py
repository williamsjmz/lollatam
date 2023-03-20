from django.contrib.auth import get_user_model, authenticate, login, logout
from django.test import TestCase, Client
from django.urls import reverse

from users.forms import UserForm, AuthForm
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

class LoginTestCase(TestCase):

    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.profile = Profile.objects.create(user=self.user)

    def test_get_login_page(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], AuthForm)

    def test_valid_login(self):
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('network:profile'))
        user = authenticate(username='testuser', password='testpass')
        self.assertIsNotNone(user)
        self.assertEqual(user, self.user)

    def test_invalid_login(self):
        response = self.client.post(reverse('users:login'), {'username': 'testuser', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIsInstance(response.context['form'], AuthForm)
        self.assertContains(response, 'Las credenciales son inválidas.')

    def test_authenticated_user_redirect(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('network:profile'))

class LogoutTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpass'
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_logout_redirects_to_login(self):
        # Log in the user before accessing the logout page
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('users:logout'))

        # Assert that the response is a redirect to the login page
        self.assertRedirects(response, reverse('users:login'))

    def test_user_logged_out(self):
        # Log in the user before accessing the logout page
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('users:logout'))

        # Assert that the user is logged out
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class VerifyEmailTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpass'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            email_verified=False,
            verification_token='testtoken'
        )

    def test_email_verified(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('users:verify_email') + f'?token={self.profile.verification_token}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('network:profile'))
        self.profile.refresh_from_db()
        self.assertTrue(self.profile.email_verified)
        self.assertIsNone(self.profile.verification_token)

    def test_invalid_token(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('users:verify_email') + '?token=invalidtoken'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('network:profile'))
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.email_verified)
        self.assertEqual(self.profile.verification_token, 'testtoken')

    def test_no_token(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('users:verify_email')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('network:profile'))
        self.profile.refresh_from_db()
        self.assertFalse(self.profile.email_verified)
        self.assertEqual(self.profile.verification_token, 'testtoken')