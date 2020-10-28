import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from polls.models import Question


class QuestionModelTests(TestCase):
    """Tests for Django model."""

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently() returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently() returns True for questions whose pub_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_past_question(self):
        """is_published() returns true if current date is before question’s publication date."""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(
            pub_date=time, end_date=timezone.now() - datetime.timedelta(days=1))
        self.assertIs(past_question.is_published(), True)

    def test_is_published_with_future_question(self):
        """is_published() return false if future date is on or after question's publication date."""
        time = timezone.now() + datetime.timedelta(days=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_can_vote_with_past_and_future_question(self):
        """can_vote() return false if voting is not allowed for this question."""
        time = timezone.now() - datetime.timedelta(days=2)
        past_question = Question(
            pub_date=time, end_date=timezone.now() - datetime.timedelta(days=1))
        self.assertIs(past_question.can_vote(), False)
        future_question = Question(pub_date=time + datetime.timedelta(
            days=5), end_date=timezone.now() + datetime.timedelta(days=10))
        self.assertIs(future_question.can_vote(), False)
