from rest_framework.authentication import SessionAuthentication

from users.methods import verify_login


class CustomSessionAuthentication(SessionAuthentication):
    def authenticate(self, request):
        ret = super().authenticate(request)
        if ret is not None:
            user, _ = ret
            verify_login(user)
        return ret
