"""Views for Polls app."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Question, Choice,Vote
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin


def index(request):
    """Show list of questions."""
    latest_question_list = Question.objects.order_by('-pub_date')
    contexts = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', contexts)


def detail(request, question_id):
    """Show detail of each selected question."""
    question = get_object_or_404(Question, pk=question_id)
    lasted_vote = question.vote_set.get(user= request.user)
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
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

