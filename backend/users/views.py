from django.contrib.auth import get_user_model
from rest_framework import exceptions as rest_exceptions
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainSlidingView

from main.mixins import ViewSetPermissionByMethodMixin
from users.serializers import CustomUserSerializer, CustomUserUpdateSerializer, CustomUserPasswordUpdateSerializer, \
    CustomTokenObtainSlidingSerializer, CustomUserForgotPasswordTokenSerializer, CustomUserForgotPasswordSerializer
from . import permissions as user_permissions
from .methods import send_email_async, invalidate_old_authentication_token
from .models import ForgotPasswordToken, CustomUser


class CustomUserViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (user_permissions.CanAccessCustomUser,)
    permission_action_classes = dict(
        create=(permissions.AllowAny,),
        list=(~permissions.AllowAny,),
        generate_forgot_password_token=(permissions.AllowAny,),
        forgot_password=(permissions.AllowAny,),
    )
    queryset = get_user_model().objects.all()
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.request.method.lower() in ['put', 'patch']:  # certain fields shouldn't be changed later
            return CustomUserUpdateSerializer
        return CustomUserSerializer

    @action(methods=['post'], detail=True, url_path='change-password', url_name='change-password')
    def change_password(self, request, uid):
        if str(uid) != str(request.user.uid):
            raise rest_exceptions.PermissionDenied('Invalid change password request')

        serializer = CustomUserPasswordUpdateSerializer(data=request.data, context=dict(request=request),
                                                        instance=request.user)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  # https://stackoverflow.com/a/31175629/5394180
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='forgot-password-token', url_name='forgot-password-token')
    def generate_forgot_password_token(self, request):
        serializer = CustomUserForgotPasswordTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = CustomUser.objects.get(email=request.data['email'])
        ForgotPasswordToken.objects.filter(user=user).delete()
        token = ForgotPasswordToken.objects.create(user=user)

        send_email_async(subject='RMP - Forgot Password Token', body='Token: {}'.format(token.token),
                         recipient_list=[user.email])
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='forgot-password', url_name='forgot-password')
    def forgot_password(self, request):
        serializer = CustomUserForgotPasswordSerializer(data=request.data, context=dict(request=request))
        serializer.is_valid(raise_exception=True)
        token = ForgotPasswordToken.objects.get(token=request.data['token'])
        user = token.user
        user.set_password(request.data['new_password'])
        user.save()
        invalidate_old_authentication_token(user)
        token.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False,
            url_path=r'verify-email/(?P<email_verification_token>[a-zA-Z0-9]{32})',
            url_name='verify-email)',
            permission_classes=[permissions.AllowAny])
    def verify_email(self, request, email_verification_token=None):
        try:
            user = get_user_model().objects.get(email_verification_token=email_verification_token)
            if user.email_verified:
                return Response(status=status.HTTP_200_OK)
            user.email_verified = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        except get_user_model().DoesNotExist as e:
            raise rest_exceptions.ValidationError('Invalid email verification token.')

    def create(self, request, *args, **kwargs):
        ret = super().create(request, *args, **kwargs)
        user = ret.data.serializer.instance
        send_email_async(subject='Email verification token', body=user.email_verification_token,
                         recipient_list=[user.email])
        return Response(status=status.HTTP_200_OK)


class CustomTokenObtainSlidingView(TokenObtainSlidingView):
    serializer_class = CustomTokenObtainSlidingSerializer
