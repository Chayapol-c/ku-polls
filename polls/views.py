"""Views for Polls app."""
import logging
import logging.config
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Question, Choice
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from mysite.settings import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('polls')

def get_client_ip(request):
    """Return ip of current user."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def login_logging(sender, request, user, **kwargs):
    """Show an formated info logging when user is logged in."""
    logger.info(f'User {user.username} with ip: {get_client_ip(request)} has log in')

@receiver(user_logged_out)
def logout_logging(sender, request, user, **kwargs):
    """Show an formated info logging when user is logged out."""
    logger.info(f'User {user.username} with ip: {get_client_ip(request)} has log out')

@receiver(user_login_failed)
def failed_login_logging(sender, request, user, **kwargs):
    """Show a warning formated info logging when user give a wrong password or username."""
    logger.warning(f'User {user.username} with ip: {get_client_ip(request)} log in failed')

def index(request):
    """Show list of questions."""
    latest_question_list = Question.objects.order_by('-pub_date')
    contexts = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', contexts)

def detail(request, question_id):
    """Show detail of each selected question."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        return redirect("polls:index")
    lasted_vote = question.vote_set.get(user=request.user)
    return render(request, 'polls/detail.html', {'question': question, 'lasted_vote': lasted_vote})


def results(request, question_id):
    """Show result of selected question."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


@login_required
def vote(request, question_id):
    """Update choice count when select."""
    user = request.user

    question = get_object_or_404(Question, pk=question_id)
    print("current user is", user.id, "login", user.username)
    print("Real name:", user.first_name, user.last_name)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        if question.vote_set.filter(user=user).exists():
            vote = question.vote_set.get(user=user)
            vote.choice = selected_choice
            vote.save()
        else:
            selected_choice.vote_set.create(user=user, question=question)
        logger.info(f"User {user.username} submit a vote for question {question.id} ")
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
