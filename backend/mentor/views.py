from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

import mentor.permissions as mentor_permissions
from main.mixins import ViewSetPermissionByMethodMixin
from mentee import permissions as mentee_permissions
from mentor.filters import MentorFilter, MentorEducationFilter, MentorResearchFilter
from mentor.models import Mentor, MentorResponsibility, MentorDepartment, MentorDesignation, MentorDiscipline, \
    MentorEducation, MentorResearch
from mentor.serializers import MentorSerializer, MentorResponsibilitySerializer, MentorDepartmentSerializer, \
    MentorDesignationSerializer, MentorDisciplineSerializer, MentorEducationSerializer, MentorResearchSerializer, \
    MentorViewSerializer
from mentorship import permissions as mentorship_permissions
from mentorship.models import MentorshipRequestStatus


class MentorViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_action_classes = dict(
        create=(~permissions.AllowAny,),  # Mentor profile creation is automated on first-login
        retrieve=(mentor_permissions.CanRetrieveMentor,),
        list=(permissions.IsAuthenticated,),
        update=(mentor_permissions.CanAccessMentor,),
        partial_update=(mentor_permissions.CanAccessMentor,),
        destroy=(~permissions.AllowAny,),  # Automatically destroyed when deleting the user-account
        find_for_mentorship=(mentorship_permissions.CanAccessMentorshipApp, mentee_permissions.IsMentee,),
    )

    queryset = Mentor.objects.all()  # Mentor object is created on first successful login only
    lookup_field = 'uid'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = MentorFilter
    search_fields = ['^user__username', '^user__first_name', '^user__last_name']

    @action(methods=['get'], detail=False, url_path='find_for_mentorship', url_name='requestable-mentors')
    def find_for_mentorship(self, request):
        """
        Return those mentors with whom the mentee does not have an existing mentorship
        or a pending mentorship request. Also applies the filter specified by the user.
        """
        cond1 = ~(Q(mentor_mentorship_requests__mentee=request.user.mentee) &
                  Q(mentor_mentorship_requests__status=MentorshipRequestStatus.REQUEST_PENDING))
        cond2 = ~Q(mentor_mentorships__mentee=request.user.mentee)
        queryset = Mentor.objects.filter(cond1, cond2,
                                         is_accepting_mentorship_requests=True,
                                         accepted_mentee_types=request.user.mentee.designation)

        queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        ret = super().update(request, *args, **kwargs)
        request.user.mentor.profile_completed = True
        request.user.mentor.save()
        return ret

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
