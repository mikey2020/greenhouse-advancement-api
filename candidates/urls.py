from django.contrib import admin
from django.urls import path, re_path
from .views import notify_user

urlpatterns = [
    re_path('tasks/$', notify_user, name="notify-all"),
    ]