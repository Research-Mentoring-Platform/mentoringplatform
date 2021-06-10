from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from main.mixins import ViewSetPermissionByMethodMixin
from users.serializers import CustomUserSerializer
from . import permissions as user_permissions


class CustomUserViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (user_permissions.CanAccessCustomUser,)
    permission_action_classes = dict(
        create=[~permissions.AllowAny],
        list=[permissions.IsAuthenticated & user_permissions.IsAdmin],  # bitwise AND is intentional
        create_mentor=[permissions.AllowAny],
        create_mentee=[permissions.AllowAny],
    )
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'uid'

    def create_user(self, request, is_mentor: bool):
        serializer = CustomUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance
        if is_mentor:
            user.is_mentor = True
        else:
            user.is_mentee = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=self.get_success_headers(serializer.data))

    # https://stackoverflow.com/a/41094241/5394180
    @action(detail=True, methods=['post'])
    def create_mentor(self, request):
        return self.create_user(request, is_mentor=True)

    @action(detail=True, methods=['post'])
    def create_mentee(self, request):
        return self.create_user(request, is_mentor=False)
