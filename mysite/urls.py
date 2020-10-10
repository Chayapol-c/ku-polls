"""Url config for mysite project."""
from django.contrib import admin
from django.urls import path, include
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', view.index),
]
