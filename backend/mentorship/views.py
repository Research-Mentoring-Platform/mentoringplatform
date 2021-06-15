from rest_framework import permissions
from rest_framework import viewsets

from mentorship.models import Education, Research
from mentorship.serializers import EducationSerializer, ResearchSerializer


class EducationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
    lookup_field = 'uid'


class ResearchViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ResearchSerializer
    queryset = Research.objects.all()
    lookup_field = 'uid'
