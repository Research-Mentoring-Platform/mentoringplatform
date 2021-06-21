from rest_framework import exceptions as rest_exceptions
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from mentorship.models import MentorshipRequest
from mentorship.serializers import MentorshipRequestSerializer, MentorshipRequestAcceptanceSerializer


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
