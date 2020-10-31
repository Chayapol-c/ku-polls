"""Django test for voting."""
import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question, Vote
from django.contrib.auth.models import User

def create_question(question_text, days):
    """
    Create a question with the given `question_text`and published the given number of `days` offset to now.

    (Negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    time_end = timezone.now() + datetime.timedelta(days=days + 10, hours=2)
    return Question.objects.create(question_text=question_text, pub_date=time, end_date=time_end)


class VotingTest(TestCase):
    """Test for voting."""

    def test_can_vote_when_authorize(self):
        """Only authorize user can vote on a question."""
        question = create_question(question_text="test question", days=-1)
        choice = question.choice_set.create(choice_text="test choice 1")
        user = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        question.vote_set.create(user=user, question=question, choice=choice)
        response = self.client.post(reverse('login'), {'username': 'test', 'password': '12test12'}, follow=True)
        url = reverse("polls:detail", args=(question.id, ))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': 1})
        self.assertEqual(Vote.objects.filter(question=question, choice=choice).count(), 1)

    def test_two_user_vote_on_same_choice(self):
        """Total count for choice will equal to 2 if two users votes on a same choice."""
        question = create_question(question_text="test question", days=-1)
        choice = question.choice_set.create(choice_text="test choice 1")
        user1 = User.objects.create_user(username='test', password='12test12', email='test@example.com')
        question.vote_set.create(user=user1, question=question, choice=choice)
        self.client.post(reverse('login'), {'username': 'test', 'password': '12test12'}, follow=True)
        self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': 1})
        user2 = User.objects.create_user(username='test2', password='12test12', email='test@example.com')
        question.vote_set.create(user=user2, question=question, choice=choice)
        self.client.post(reverse('login'), {'username': 'test2', 'password': '12test12'}, follow=True)
        self.client.post(reverse('polls:vote', args=(question.id,)), {'choice': 1})
        self.assertEqual(Vote.objects.filter(question=question, choice=choice).count(), 2)
