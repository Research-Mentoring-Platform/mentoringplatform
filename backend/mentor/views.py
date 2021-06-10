from rest_framework import viewsets
from main.mixins import ViewSetPermissionByMethodMixin


class MentorViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    pass  # TODO
