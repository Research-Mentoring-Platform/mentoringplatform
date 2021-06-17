from django.contrib.auth import get_user_model
from rest_framework import exceptions as rest_exceptions
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainSlidingView

from main.mixins import ViewSetPermissionByMethodMixin
from users.serializers import CustomUserSerializer, CustomUserUpdateSerializer, CustomUserPasswordUpdateSerializer, \
    CustomTokenObtainSlidingSerializer
from . import permissions as user_permissions
from .methods import send_email_async


class CustomUserViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (user_permissions.CanAccessCustomUser,)
    permission_action_classes = dict(
        create=[permissions.AllowAny],
        list=[permissions.IsAuthenticated & user_permissions.IsAdmin],  # bitwise AND is intentional
    )
    queryset = get_user_model().objects.all()
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.request.method.lower() in ['put', 'patch']:  # certain fields shouldn't be changed later
            return CustomUserUpdateSerializer
        return CustomUserSerializer

    @action(methods=['post'], detail=False, url_path='update-password', url_name='update-password',
            permission_classes=[user_permissions.CanChangeCustomUserPassword])
    def update_password(self, request):
        serializer = CustomUserPasswordUpdateSerializer(data=request.data, context=dict(request=request),
                                                        instance=request.user)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  # https://stackoverflow.com/a/31175629/5394180
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False,
            url_path=r'verify-email/(?P<email_verification_token>[a-zA-Z0-9]{32})',
            url_name='verify-email)',
            permission_classes=[permissions.AllowAny])
    def verify_email(self, request, email_verification_token=None):
        try:
            user = get_user_model().objects.get(email_verification_token=email_verification_token)
            if user.email_verified:
                raise rest_exceptions.ValidationError('User is already verified.')
            user.email_verified = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist:
            raise rest_exceptions.ValidationError('Invalid email verification token.')

    def create(self, request, *args, **kwargs):
        ret = super().create(request, *args, **kwargs)
        user = ret.data.serializer.instance
        send_email_async(subject='Email verification token', body=user.email_verification_token,
                         recipient_list=[user.email, ])
        return Response(status=status.HTTP_200_OK)


class CustomTokenObtainSlidingView(TokenObtainSlidingView):
    serializer_class = CustomTokenObtainSlidingSerializer
