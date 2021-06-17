import threading

from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string
from rest_framework import exceptions as rest_exceptions

from mentee.models import Mentee
from mentor.models import Mentor


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


def verify_login(user):
    """
    This served to both DRF's token-auth and session-auth
    """
    if user.is_admin and (not user.is_mentor):
        raise rest_exceptions.ValidationError('Non-mentor admins should use backend admin-login instead')

    if not user.email_verified:
        raise rest_exceptions.ValidationError('Email not verified.')

    if user.is_mentor:
        if not hasattr(user, 'mentor'):
            Mentor.objects.create(user=user)
    else:  # is mentee
        if not hasattr(user, 'mentee'):
            Mentee.objects.create(user=user)
