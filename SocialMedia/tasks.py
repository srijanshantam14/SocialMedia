from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.decorators import tasks


from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template

@tasks
def SendEmail(email,msg):
    from_email=settings.EMAIL_HOST_USER
    to_email = [email]
    #html =get_template("mail.html").render("msg":msg)
    html="<h1>Email</h1>"
    sub ="Techblog -New Like"
    send_mail(sub,msg,from_email, to_email,html_message=html)