from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

import mentor.permissions as mentor_permissions
from main.mixins import ViewSetPermissionByMethodMixin
from mentor.filters import MentorFilter, MentorEducationFilter, MentorResearchFilter
from mentor.models import Mentor, MentorResponsibility, MentorDepartment, MentorDesignation, MentorDiscipline, \
    MentorEducation, MentorResearch
from mentor.serializers import MentorSerializer, MentorResponsibilitySerializer, MentorDepartmentSerializer, \
    MentorDesignationSerializer, MentorDisciplineSerializer, MentorEducationSerializer, MentorResearchSerializer


class MentorViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (mentor_permissions.CanAccessMentor,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,),
        destroy=(~permissions.AllowAny,),
        create=(~permissions.AllowAny,)
    )
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = MentorFilter
    search_fields = ['^user__username', '^user_first_name', '^user_last_name']


class MentorResponsibilityViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,)
    )
    queryset = MentorResponsibility.objects.all()
    serializer_class = MentorResponsibilitySerializer
    lookup_field = 'uid'


class MentorDepartmentViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,)
    )
    queryset = MentorDepartment.objects.all()
    serializer_class = MentorDepartmentSerializer
    lookup_field = 'uid'


class MentorDesignationViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,)
    )
    queryset = MentorDesignation.objects.all()
    serializer_class = MentorDesignationSerializer
    lookup_field = 'uid'


class MentorDisciplineViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        list=(permissions.IsAuthenticated,),
        retrieve=(permissions.IsAuthenticated,)
    )
    queryset = MentorDiscipline.objects.all()
    serializer_class = MentorDisciplineSerializer
    lookup_field = 'uid'


class MentorEducationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MentorEducationSerializer
    queryset = MentorEducation.objects.all()
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MentorEducationFilter


class MentorResearchViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MentorResearchSerializer
    queryset = MentorResearch.objects.all()
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MentorResearchFilter
