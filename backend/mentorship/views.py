from rest_framework import exceptions as rest_exceptions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from mentorship.models import MentorshipRequest, Mentorship, Meeting
from mentorship.serializers import MentorshipRequestSerializer, MentorshipRequestAcceptanceSerializer, \
    MentorshipSerializer, MeetingSerializer


class MentorshipViewSet(viewsets.ModelViewSet):
    queryset = Mentorship.objects.all()
    serializer_class = MentorshipSerializer
    lookup_field = 'uid'

    def create(self, request, *args, **kwargs):
        # Mentorship is created by accepting a mentorship request
        raise rest_exceptions.PermissionDenied('Mentorship cannot be created')


class MentorshipRequestViewSet(viewsets.ModelViewSet):
    queryset = MentorshipRequest.objects.all()
    serializer_class = MentorshipRequestSerializer
    lookup_field = 'uid'

    def partial_update(self, request, *args, **kwargs):
        raise rest_exceptions.PermissionDenied('Update not allowed.')

    def update(self, request, *args, **kwargs):
        raise rest_exceptions.PermissionDenied('Update not allowed.')

    @action(methods=['post'], detail=True, url_path='respond', url_name='respond-to-request')
    def respond(self, request):
        serializer = MentorshipRequestAcceptanceSerializer(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    lookup_field = 'uid'
