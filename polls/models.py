"""Config for Django model."""
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Django model Object for questions."""

    class Meta:
        permissions = (('can_vote', 'can submit a vote'),
                       ('can_view_result', 'can review poll results'))

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('ending date ')

    def __str__(self):
        """Return string representation for Question."""
        return self.question_text

    def was_published_recently(self):
        """Return true if question is published."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Return true if pub date is before than current date."""
        now = timezone.now()
        return self.pub_date <= now

    def can_vote(self):
        """Return true if question is published and it before end date."""
        now = timezone.now()
        return now <= self.end_date and self.is_published()

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Django model Object for choices."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Return string representation for Choice."""
        return self.choice_text

    @property
    def votes(self):
        return self.question.vote_set.filter(choice=self).count()


class Vote(models.Model):
    """Django model Object for vote."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=0)

    def __str__(self):
        return f'{self.question.question_text} voted'
