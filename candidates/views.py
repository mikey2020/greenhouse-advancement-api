from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .task import myTask
# Create your views here.

from background_task import background
from django.contrib.auth.models import User


# @background(schedule=60)
@api_view()
def notify_user(request, version):
    # lookup user by id and send them a message
    user = User.objects.get(pk=request.user.pk)
    # user.email_user('Here is a notification', 'You have been notified')

    # print(' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>I got here ', user)
    myTask()
    return Response({"message": "Hello for today! See you tomorrow!"})

