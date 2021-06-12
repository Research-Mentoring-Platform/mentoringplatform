from rest_framework import viewsets, permissions

from main.mixins import ViewSetPermissionByMethodMixin
from mentee import permissions as mentee_permissions
from mentee.models import Mentee
from mentee.serializers import MenteeSerializer

from users import permissions as user_permissions


class MenteeViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (mentee_permissions.CanAccessMentee,)
    permission_action_classes = dict(
        list=(user_permissions.IsAdmin,),
        destroy=(~permissions.AllowAny,),  # This is automated, linked with the user model
        create=(~permissions.AllowAny,)  # This is automated, linked with the user model
    )

    lookup_field = 'uid'
    queryset = Mentee.objects.all()
    serializer_class = MenteeSerializer
