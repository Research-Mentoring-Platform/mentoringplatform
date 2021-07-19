from django.utils import timezone
from rest_framework import exceptions as rest_exceptions
from rest_framework import permissions as rest_permissions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from main.mixins import ViewSetPermissionByMethodMixin
from mentee import permissions as mentee_permissions
from mentor import permissions as mentor_permissions
from mentorship.models import MentorshipRequest, Mentorship, Meeting, MeetingSummary, Milestone, \
    MentorshipRequestStatus, MentorshipStatus
from mentorship.serializers import MentorshipRequestSerializer, MentorshipRequestAcceptanceSerializer, \
    MentorshipSerializer, MeetingSerializer, MeetingSummarySerializer, MilestoneSerializer
from . import permissions as mentorship_permissions


class MentorshipViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_action_classes = dict(
        create=(~rest_permissions.AllowAny,),
        retrieve=(mentorship_permissions.CanAccessMentorship,),
        list=(mentorship_permissions.CanAccessMentorshipApp,),  # get_queryset also modified accordingly
        update=(~rest_permissions.AllowAny,),  # Can only be terminated/finished using the corresponding methods
        partial_update=(~rest_permissions.AllowAny,),
        destroy=(~rest_permissions.AllowAny,),  # For record-keeping
        finish=(mentorship_permissions.CanAccessMentorship,),
        terminate=(mentorship_permissions.CanAccessMentorship,),
    )
    queryset = Mentorship.objects.all()
    serializer_class = MentorshipSerializer
    lookup_field = 'uid'

    def create(self, request, *args, **kwargs):
        # Mentorship is created by accepting a mentorship request
        raise rest_exceptions.PermissionDenied('Mentorship cannot be created')

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_mentor:
                return Mentorship.objects.filter(mentor=self.request.user.mentor)
            elif self.request.user.is_mentee:
                return Mentorship.objects.filter(mentee=self.request.user.mentee)
            # TODO Check for admin by overriding permissions.IsAuthenticated

        return super().get_queryset()

    @action(methods=['post'], detail=True, url_path='finish', url_name='finish-mentorship')
    def finish(self, request):
        obj = self.get_object()
        if obj.status == MentorshipStatus.ONGOING:
            obj.status = MentorshipStatus.FINISHED
            obj.end_date = timezone.now()
            obj.save()
            return Response(status=status.HTTP_200_OK)

        raise rest_exceptions.PermissionDenied('Cannot change status of a non-ongoing mentorship.')

    @action(methods=['post'], detail=True, url_path='terminate', url_name='terminate-mentorship')
    def terminate(self, request):
        obj = self.get_object()
        if obj.status == MentorshipStatus.ONGOING:
            obj.status = MentorshipStatus.TERMINATED
            obj.end_date = timezone.now()
            obj.save()
            return Response(status=status.HTTP_200_OK)

        raise rest_exceptions.PermissionDenied('Cannot change status of a non-ongoing mentorship.')


class MentorshipRequestViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_action_classes = dict(
        create=(mentorship_permissions.CanAccessMentorshipApp, mentee_permissions.IsMentee,),
        # TODO check if , is enforcing all the permissions
        retrieve=(mentorship_permissions.CanAccessMentorshipRequest,),
        list=(mentorship_permissions.CanAccessMentorshipApp,),  # get_queryset also modified accordingly
        update=(~rest_permissions.AllowAny,),  # Can only be accepted/rejected using the respond method
        partial_update=(~rest_permissions.AllowAny,),
        destroy=(mentorship_permissions.CanAccessMentorshipRequest, mentee_permissions.IsMentee,),
        # Only mentee can cancel a `pending` request
        respond=(mentorship_permissions.CanAccessMentorshipRequest, mentor_permissions.IsMentor,),
        get_pending_requests=(mentorship_permissions.CanAccessMentorshipRequest,)
        # TODO check if , is enforcing all the permissions
    )
    queryset = MentorshipRequest.objects.all()
    serializer_class = MentorshipRequestSerializer
    lookup_field = 'uid'

    def partial_update(self, request, *args, **kwargs):
        raise rest_exceptions.PermissionDenied('Update not allowed.')

    def update(self, request, *args, **kwargs):
        raise rest_exceptions.PermissionDenied('Update not allowed.')

    def destroy(self, request, *args, **kwargs):
        # User is a mentee (enforced by the IsMentee permission)
        obj = self.get_object()
        if obj.status != MentorshipRequestStatus.REQUEST_PENDING:
            raise rest_exceptions.PermissionDenied('Cannot delete a non-pending request.')

        return super().destroy(request, *args, **kwargs)

    @action(methods=['post'], detail=True, url_path='respond', url_name='respond-to-request')
    def respond(self, request, uid):
        serializer = MentorshipRequestAcceptanceSerializer(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='pending', url_name='pending-requests')
    def get_pending_requests(self, request):
        """
        Return those mentors with whom the mentee does not have an existing mentorship
        or a pending mentorship request
        """
        queryset = None
        if request.user.is_mentor:
            queryset = MentorshipRequest.objects.filter(mentor=request.user.mentor,
                                                        status=MentorshipRequestStatus.REQUEST_PENDING)
        elif request.user.is_mentee:
            queryset = MentorshipRequest.objects.filter(mentee=request.user.mentee,
                                                        status=MentorshipRequestStatus.REQUEST_PENDING)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_mentor:
                return MentorshipRequest.objects.filter(mentor=self.request.user.mentor)
            elif self.request.user.is_mentee:
                return MentorshipRequest.objects.filter(mentee=self.request.user.mentee)
            # TODO Check for admin by overriding permissions.IsAuthenticated

        return super().get_queryset()


class MeetingViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_action_classes = dict(
        create=(mentorship_permissions.CanAccessMentorshipApp,),
        retrieve=(mentorship_permissions.CanAccessMeeting,),
        list=(mentorship_permissions.CanAccessMentorshipApp,),  # get_queryset also modified accordingly
        update=(mentorship_permissions.CanAccessMeeting,),
        partial_update=(mentorship_permissions.CanAccessMeeting,),
        destroy=(mentorship_permissions.CanAccessMeeting,),
    )
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    lookup_field = 'uid'

    def destroy(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.date_time < timezone.now():
            raise rest_exceptions.PermissionDenied('Cannot delete a past meeting.')

        return super().destroy(request, *args, **kwargs)

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_mentor:
                return Meeting.objects.filter(mentorship__mentor=self.request.user.mentor)
            elif self.request.user.is_mentee:
                return Meeting.objects.filter(mentorship__mentee=self.request.user.mentee)

        return super().get_queryset()


class MeetingSummaryViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_action_classes = dict(
        create=(mentorship_permissions.CanAccessMentorshipApp,),
        retrieve=(mentorship_permissions.CanAccessMeetingSummary,),
        list=(mentorship_permissions.CanAccessMentorshipApp,),  # get_queryset also modified accordingly
        update=(mentorship_permissions.CanAccessMeetingSummary,),
        partial_update=(mentorship_permissions.CanAccessMeetingSummary,),
        destroy=(mentorship_permissions.CanAccessMeetingSummary,),
    )
    queryset = MeetingSummary.objects.all()
    serializer_class = MeetingSummarySerializer
    lookup_field = 'uid'

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_mentor:
                return MeetingSummary.objects.filter(meeting__mentorship__mentor=self.request.user.mentor)
            elif self.request.user.is_mentee:
                return MeetingSummary.objects.filter(meeting__mentorship__mentee=self.request.user.mentee)

        return super().get_queryset()


class MilestoneViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_action_classes = dict(
        create=(mentorship_permissions.CanAccessMentorshipApp,),
        retrieve=(mentorship_permissions.CanAccessMilestone,),
        list=(mentorship_permissions.CanAccessMentorshipApp,),  # get_queryset also modified accordingly
        update=(mentorship_permissions.CanAccessMilestone, mentor_permissions.IsMentor,),
        partial_update=(mentorship_permissions.CanAccessMilestone, mentor_permissions.IsMentor,),
        destroy=(mentorship_permissions.CanAccessMilestone, mentor_permissions.IsMentor,),
    )
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    lookup_field = 'uid'

    def get_queryset(self):
        if self.action == 'list':
            if self.request.user.is_mentor:
                return Milestone.objects.filter(mentorship__mentor=self.request.user.mentor)
            elif self.request.user.is_mentee:
                return Milestone.objects.filter(mentorship__mentee=self.request.user.mentee)

        return super().get_queryset()
