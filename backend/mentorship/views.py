from rest_framework import permissions
from rest_framework import viewsets

from mentorship.models import Education
from mentorship.serializers import EducationSerializer


class EducationViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = EducationSerializer
    queryset = Education.objects.all()
