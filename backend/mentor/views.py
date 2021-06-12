from rest_framework import viewsets
from main.mixins import ViewSetPermissionByMethodMixin
import mentor.permissions as mentor_permissions
from rest_framework import permissions

from mentor.models import Mentor
from mentor.serializers import MentorSerializer


class MentorViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (mentor_permissions.CanAccessMentor,)
    permission_access_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,),
        destroy=(permissions.IsAdminUser,),
        create=(permissions.IsAdminUser,)
    )
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    lookup_field = 'uid'
