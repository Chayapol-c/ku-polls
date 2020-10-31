"""Django test for voting."""
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question
from django.test import Client
from django.contrib.auth.models import User


class VotingTest(TestCase):
    """ """

    def test_can_vote_when_authorize(self):
        """ """
        user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        response = self.client.post('/account/login/', {'username': 'test', 'password': '12test12'}, follow=True)
        url = reverse("polls:index")

    def test_can_see_latest_vote(self):
        pass

    def test_vote_can_replace_last_one(self):
        pass
