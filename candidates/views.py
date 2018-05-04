from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .task import myTask
import requests
import json

# Create your views here.

#from background_task import background
from django.contrib.auth.models import User


# @background(schedule=60)
@api_view()
def notify_user(request, version):
    print(request.user)
    # lookup user by id and send them a message
    user = User.objects.all()
    # user.email_user('Here is a notification', 'You have been notified')

    # print(' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>I got here ', user)
    myTask()
    return Response({"message": "Hello for today! See you tomorrow!"})

@api_view()
def get_user_application_id(request):
    job_id = request.GET.get('job_id', '')
    user_email = request.GET.get('email', '')
    print(job_id, user_email)
    headers = {"Authorization": "Basic N2U5OTgzYTllNjM1NGE0NDFiMzQ5YWYyNjFhYjQ4MmEtMQ=="}
    response = requests.get('https://harvest.greenhouse.io/v1/candidates?job_id=' + job_id + '&email=' + user_email, headers=headers)
    application_id = {x["first_name"] + " " + x["last_name"]: x["applications"][0]["id"] for x in response.json()}
    print(application_id)
    return Response(application_id)

@api_view()
def get_jobs(request):
    date = request.GET.get('created_after', '')
    headers = {"Authorization": "Basic N2U5OTgzYTllNjM1NGE0NDFiMzQ5YWYyNjFhYjQ4MmEtMQ=="}
    response = requests.get('https://harvest.greenhouse.io/v1/jobs?created_after=' + date, headers=headers)
    return Response(response.json())

@api_view()
def get_job_stages_id(request):
    job_id = request.GET.get('job_id', '')
    headers = {"Authorization": "Basic N2U5OTgzYTllNjM1NGE0NDFiMzQ5YWYyNjFhYjQ4MmEtMQ=="}
    response = requests.get('https://harvest.greenhouse.io/v1/jobs/' + job_id + '/stages', headers=headers)
    print(response.json())
    response_ids = response.json()
    stages_id = {y["name"]: y["id"]  for y in response_ids}
    print(stages_id)
    return Response(stages_id)

@api_view(['POST'])
def advance_application(request):
    if request.method == 'POST':
        headers = {
            "Authorization": "Basic N2U5OTgzYTllNjM1NGE0NDFiMzQ5YWYyNjFhYjQ4MmEtMQ==",
            "On-Behalf-Of": "71037"
        }
        app_id = request.GET.get('app_id', '')
        payload = request.body.decode("utf-8")
        payload = json.loads(payload)
        response = requests.post('https://harvest.greenhouse.io/v1/applications/' + app_id + '/advance',
                   headers=headers, data=json.dumps(payload)
        )
        print(response.status_code)
        return Response(response.json())

