from django.shortcuts import render
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import csv
import time
import re
import os

from django.shortcuts import render
from bluckmail.settings import EMAIL_HOST_USER
from django.core.mail import send_mail

# Create your views here.

def index(request):
    return render(request,'home.html')

def mail(request):
    sender_mail = request.POST.get('sender_email')
    Password = request.POST.get('Password')
    Subject = request.POST.get('Subject')
    myfile = request.FILES['myfile']
    data = myfile.read()
    
    with open('sample.csv','w') as f:
        f.write(data.decode())
    f.close()

    
    sender_email = "haripriyamax1427@gmail.com"
    password = "tlsleabaxjjryjjw"
    message = MIMEMultipart("alternative")
    message["Subject"] = "Testing App"
    message["From"] = sender_email
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context)
    server.ehlo()
    server.login(sender_email, password)

    count = 0
    with open("sample.csv") as file:
        reader = csv.reader(file)
        next(reader)    
        for  email in reader:
            for check in email:
                pat = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'
                obj = re.match(pat, check)
                if obj:
                    print("Valid Email")
                else:
                    print("Invalid")
            
            subject = 'Dont Mind This Mail'
            message = 'Experimenting with my new django mini project. Thank you!'
            send_mail(subject, message, EMAIL_HOST_USER, [subject], fail_silently=False)

            count += 1
            print(str(count)," Sent to ",email)
            if(count%80 == 0):
                server.quit()
                print("Server cooldown for 100 seconds")
                time.sleep(2000)
                server.ehlo()
                server.login(sender_email, password)
    server.quit()
    return render(request,'home.html')

