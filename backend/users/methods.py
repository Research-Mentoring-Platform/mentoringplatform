import threading

from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string


def generate_email_verification_token():
    return get_random_string(length=32)


# https://stackoverflow.com/a/4447147/5394180
class EmailThread(threading.Thread):
    def __init__(self, subject, body, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.body = body
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMessage(subject=self.subject, body=self.body, to=self.recipient_list)
        msg.content_subtype = 'html'
        msg.send()


def send_email_async(subject, body, recipient_list):
    EmailThread(subject, body, recipient_list).start()
