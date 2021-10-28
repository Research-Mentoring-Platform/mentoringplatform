from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.core.exceptions import ValidationError
from rest_framework.authentication import SessionAuthentication
from rest_framework import exceptions as rest_exceptions

from users.methods import verify_login


class CustomDRFSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        ret = super().authenticate(request)
        if ret is not None:
            user, _ = ret
            verify_login(user)
        return ret


class CustomDjangoTestsSessionAuthentication(ModelBackend):
    def authenticate(self, request, **kwargs):
        user = super().authenticate(request, **kwargs)
        if user is not None:
            try:
                verify_login(user)
            except rest_exceptions.ValidationError as ve:
                raise ValidationError(str(ve))
        return user
