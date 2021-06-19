from rest_framework import viewsets

from mentorship.models import MentorshipRequest


class MentorshipRequestViewSet(viewsets.ModelViewSet):
    queryset = MentorshipRequest.objects.all()
    lookup_field = 'uid'
