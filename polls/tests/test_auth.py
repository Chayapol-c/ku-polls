"""Django test for User Authentication."""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthenticationTest(TestCase):
    """ """

    def test_user_can_login(self):
        """Logged in user can see greeting word 'Welcome back (username)' on index page."""
        user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        user.save()
        response = self.client.post('/account/login/', {'username': 'test', 'password': '12test12'}, follow=True)
        self.assertEqual(response.status_code, 200)
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(url, '/polls/')
        self.assertContains(response, "Welcome back, test")

    def test_user_can_logout(self):
        """User will redirect to index page after logged out."""
        user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        response = self.client.post('/account/login/', {'username': 'test', 'password': '12test12'}, follow=True)
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertContains(response, "Welcome back, test")
        self.client.logout()
        url = reverse("polls:index")
        response = self.client.get(url)
        self.assertContains(response, "Please")
