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
    MentorDesignationSerializer, MentorDisciplineSerializer, MentorEducationSerializer, MentorResearchSerializer, \
    MentorViewSerializer


class MentorViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_action_classes = dict(
        create=(~permissions.AllowAny,),  # Mentor profile creation is automated on first-login
        retrieve=(mentor_permissions.CanRetrieveMentor,),
        list=(permissions.IsAuthenticated,),
        update=(mentor_permissions.CanAccessMentor,),
        partial_update=(mentor_permissions.CanAccessMentor,),
        destroy=(~permissions.AllowAny,),  # Automatically destroyed when deleting the user-account
    )

    queryset = Mentor.objects.all()  # Mentor object is created on first successful login only
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = MentorFilter
    search_fields = ['^user__username', '^user__first_name', '^user__last_name']

    def get_queryset(self):
        if self.action == 'list':
            return Mentor.objects.filter(is_verified=True)  # Only return list of admin-verified mentors
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return MentorViewSerializer
        return MentorSerializer


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


class MentorEducationViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    permission_action_classes = dict(
        # The serializer's overridden validate ensures that the mentor themselves are modifying/creating their
        # education only
        create=(mentor_permissions.IsMentor,),
        update=(mentor_permissions.CanAccessMentorEducation,),
        partial_update=(mentor_permissions.CanAccessMentorEducation,),
        destroy=(mentor_permissions.CanAccessMentorEducation,)
    )

    serializer_class = MentorEducationSerializer
    queryset = MentorEducation.objects.all()
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MentorEducationFilter


class MentorResearchViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    permission_action_classes = dict(
        # The serializer's overridden validate ensures that the mentor themselves are modifying/creating their
        # education only
        create=(mentor_permissions.IsMentor,),
        update=(mentor_permissions.CanAccessMentorResearch,),
        partial_update=(mentor_permissions.CanAccessMentorResearch,),
        destroy=(mentor_permissions.CanAccessMentorResearch,)
    )

    serializer_class = MentorResearchSerializer
    queryset = MentorResearch.objects.all()
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MentorResearchFilter
