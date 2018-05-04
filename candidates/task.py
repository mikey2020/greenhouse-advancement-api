import datetime
import celery

import smtplib
 
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
    print('This wasn\'t so difficult')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("michael.eboagu@andela.com", "michael2017")
    
    msg = "Testing celery ..............."
    server.sendmail("michael.eboagu@andela.com", "taiwo.sokunbi@andela.com", msg)
    server.quit()