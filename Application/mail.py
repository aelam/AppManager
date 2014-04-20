__author__ = 'ryan'

from models import Package
from django.core.mail import EmailMessage

def send_mail_with_new_pack(package):
    # package.
    try:
        email = EmailMessage('Hello', 'World', to=['wanglun02@gmail.com'])
        email.send()
    finally:
        print("sending mail")

