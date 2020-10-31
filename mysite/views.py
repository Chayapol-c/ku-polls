"""Views for mysite project."""

from django.shortcuts import redirect


def index(reqest):
    """Redirect to index page."""
    return redirect("polls:index")
