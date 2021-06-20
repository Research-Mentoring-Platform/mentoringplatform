from rest_framework import viewsets

from mentorship.models import MentorshipRequest
from mentorship.serializers import MentorshipRequestSerializer


class MentorshipRequestViewSet(viewsets.ModelViewSet):
    queryset = MentorshipRequest.objects.all()
    serializer_class = MentorshipRequestSerializer
    lookup_field = 'uid'
