from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.mixins import ViewSetPermissionByMethodMixin
from users.serializers import CustomUserSerializer, CustomUserUpdateSerializer, CustomUserPasswordUpdateSerializer
from . import permissions as user_permissions


class CustomUserViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (user_permissions.CanAccessCustomUser,)
    permission_action_classes = dict(
        create=[permissions.AllowAny],
        list=[permissions.IsAuthenticated & user_permissions.IsAdmin],  # bitwise AND is intentional
    )
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.request.method.lower() in ['put', 'patch']:  # certain fields shouldn't be changed later
            return CustomUserUpdateSerializer
        return self.serializer_class

    @action(methods=['post'], detail=False, url_path='update-password', url_name='update-password',
            permission_classes=[user_permissions.CanChangeCustomUserPassword])
    def update_password(self, request):
        serializer = CustomUserPasswordUpdateSerializer(data=request.data, context=dict(request=request),
                                                        instance=request.user)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)  # https://stackoverflow.com/a/31175629/5394180
        return Response(status=status.HTTP_200_OK)
