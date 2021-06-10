from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import viewsets

from main.mixins import ViewSetPermissionByMethodMixin
from users.serializers import CustomUserSerializer, CustomUserUpdateSerializer
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
        return CustomUserSerializer
