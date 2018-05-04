from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .task import myTask
import requests
import json
import os

import datetime
import celery
import smtplib

# Create your views here.

#from background_task import background
from django.contrib.auth.models import User

emails = [
     "sokunbitaiwo82@gmail.com",
     "dannytebj@gmail.com",
     "superdafe@gmail.com",
     "fob1493@gmail.com"
]

all_user_ids = []
# from celery import shared_task

@celery.decorators.periodic_task(run_every=datetime.timedelta(minutes=1)) # here we assume we want it to be run every 5 mins
def myTask():
    # Do something here
    # like accessing remote apis,
    # calculating resource intensive computational data
    # and store in cache
    # or anything you please
    # response = requests.get('https://google.com')
    # print(response.status_code)
    get_user_application_id
    print('This wasn\'t so difficult')
    
    

# @background(schedule=60)
@api_view()
def notify_user(request, version):
    # print(request.user)
    # lookup user by id and send them a message
    user = User.objects.all()
    # user.email_user('Here is a notification', 'You have been notified')
    myTask()
    # print(' >>>>>>>>>>>>>>>>>>>>>>>>>>>>>I got here ', user)
    return Response({"message": "Hello for today! See you tomorrow!"})

@api_view()
def get_user_application_id(request):
    job_id = request.GET.get('job_id', '')
    #user_email = request.GET.get('email', '')
    headers = {"Authorization": "Basic N2U5OTgzYTllNjM1NGE0NDFiMzQ5YWYyNjFhYjQ4MmEtMQ=="}
    for email in emails:
        response = requests.get('https://harvest.greenhouse.io/v1/candidates?job_id=' + job_id + '&email=' + email, headers=headers)
        application_id = {x["first_name"] + " " + x["last_name"]: x["applications"][0]["id"] for x in response.json()}
        all_user_ids.append(application_id)


    return Response(all_user_ids)

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
    response_ids = response.json()
    stages_id = {y["name"]: y["id"]  for y in response_ids}
    return Response(stages_id)

@api_view(['POST'])
def advance_application(request):
    if request.method == 'POST':
        headers = {
            "Authorization": "Basic N2U5OTgzYTllNjM1NGE0NDFiMzQ5YWYyNjFhYjQ4MmEtMQ==",
            "On-Behalf-Of": "71037"
        }
        payload = request.body.decode("utf-8")
        payload = json.loads(payload)
        all_responses = []
        for user in all_user_ids:
            for key, value in user.items():
                response = requests.post('https://harvest.greenhouse.io/v1/applications/' + str(value) + '/advance',
                        headers=headers, data=json.dumps(payload)
                )
                all_responses.append(response.json())
        send_mail("taiwo.sokunbi@andela.com")
        return Response(all_responses)

def send_mail(receiver_email):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(os.environ.get('EMAIL'), os.environ.get('PASSWORD'))
    
    msg = "All candidates have been moved to the next stage"
    server.sendmail(os.environ.get('EMAIL'), receiver_email, msg)
    server.quit()

