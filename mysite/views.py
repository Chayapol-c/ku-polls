"""Views for mysite project."""

from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def index(reqest):
    """Redirect to index page."""
    return redirect("polls:index")


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password')
            user = AuthenticationForm(username=username, password=raw_passwd)
            # login(request, user)
            return redirect('polls')
        # what if form is not valid?
        # we should display a message in signup.html
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
