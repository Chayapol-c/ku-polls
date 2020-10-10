"""Views for Polls app."""
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Question, Choice
from django.contrib import messages


def index(request):
    """Show list of questions."""
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    """Show detail of each selected question."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    """Show result of selected question."""
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    """Update choice count when select."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def vote_for_poll(request, question_id):
    """Show error message and redirect to index page if question is not allowed."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, "This Question can not vote")
        return redirect('polls:index')
    return render(request, 'polls/detail.html', {'question': question})
