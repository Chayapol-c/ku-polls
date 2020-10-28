"""Url config for mysite project."""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('', views.index),
    path('account/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
]
