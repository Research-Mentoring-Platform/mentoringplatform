from rest_framework import viewsets, permissions

from main.mixins import ViewSetPermissionByMethodMixin
from mentee import permissions as mentee_permissions
from mentee.models import Mentee, MenteeDesignation, MenteeDepartment, MenteeDiscipline
from mentee.serializers import MenteeSerializer, MenteeDepartmentSerializer, MenteeDisciplineSerializer, \
    MenteeDesignationSerializer

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


class MenteeDepartmentViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,)
    )
    queryset = MenteeDepartment.objects.all()
    serializer_class = MenteeDepartmentSerializer
    lookup_field = 'uid'


class MenteeDesignationViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,)
    )
    queryset = MenteeDesignation.objects.all()
    serializer_class = MenteeDesignationSerializer
    lookup_field = 'uid'


class MenteeDisciplineViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,)
    )
    queryset = MenteeDiscipline.objects.all()
    serializer_class = MenteeDisciplineSerializer
    lookup_field = 'uid'
