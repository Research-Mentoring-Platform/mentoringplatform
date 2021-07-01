from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions as rest_exceptions
from rest_framework import viewsets, permissions

from main.mixins import ViewSetPermissionByMethodMixin
from mentee import permissions as mentee_permissions
from mentee.filters import MenteeEducationFilter, MenteeResearchFilter
from mentee.models import Mentee, MenteeDesignation, MenteeDepartment, MenteeDiscipline, MenteeEducation, MenteeResearch
from mentee.serializers import MenteeSerializer, MenteeDepartmentSerializer, MenteeDisciplineSerializer, \
    MenteeDesignationSerializer, MenteeEducationSerializer, MenteeResearchSerializer


class MenteeViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (~permissions.AllowAny,)
    permission_action_classes = dict(
        retrieve=(mentee_permissions.CanRetrieveMentee,),
        update=(mentee_permissions.CanAccessMentee,),
        partial_update=(mentee_permissions.CanAccessMentee,),
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


class MenteeEducationViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (mentee_permissions.CanAccessMenteeEducation,)
    permission_action_classes = dict(
        create=(mentee_permissions.IsMentee,),
        retrieve=(mentee_permissions.CanRetrieveMenteeEducation,),
        list=(permissions.IsAuthenticated,)
    )
    serializer_class = MenteeEducationSerializer
    queryset = MenteeEducation.objects.all()
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MenteeEducationFilter

    def get_queryset(self):
        if self.action == 'list':
            pass  # TODO continue from here

    def list(self, request, *args, **kwargs):
        """
        The filterset_class enforces it to have the query-parameter: mentee
        """
        ret = super().list(request, *args, **kwargs)
        if request.user.is_mentor:
            mentee = Mentee.objects.get(uid=request.query_params.mentee)
            if mentee_permissions.CanRetrieveMentee().has_object_permission(request, self, mentee):
                return MenteeEducation.objects.filter(mentee=mentee)
            raise rest_exceptions.PermissionDenied('You cannot view the education list of the requested mentee.')
        elif request.user.is_mentee:
            return MenteeEducation.objects.filter()
        raise rest_exceptions.PermissionDenied('You cannot view')


class MenteeResearchViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = MenteeResearchSerializer
    queryset = MenteeResearch.objects.all()
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MenteeResearchFilter
