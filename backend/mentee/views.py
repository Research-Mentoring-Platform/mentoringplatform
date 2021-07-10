from rest_framework import exceptions as rest_exceptions, status
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from main.mixins import ViewSetPermissionByMethodMixin
from mentee import permissions as mentee_permissions
from mentee.models import Mentee, MenteeDesignation, MenteeDepartment, MenteeDiscipline, MenteeEducation, MenteeResearch
from mentee.serializers import MenteeSerializer, MenteeDepartmentSerializer, MenteeDisciplineSerializer, \
    MenteeDesignationSerializer, MenteeEducationSerializer, MenteeResearchSerializer, MenteeViewSerializer


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

    def update(self, request, *args, **kwargs):
        ret = super().update(request, *args, **kwargs)
        request.user.mentee.profile_completed = True
        request.user.mentee.save()
        return ret

    def get_serializer_class(self):
        if self.request.method.lower() == 'get':
            return MenteeViewSerializer
        return MenteeSerializer


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

    def get_queryset(self):
        if self.action != 'list':
            return super().get_queryset()

        mentee = Mentee.objects.get(uid=self.request.query_params['mentee'])
        if self.request.user.is_mentor:
            if mentee_permissions.CanRetrieveMentee().has_object_permission(self.request, self, mentee):
                return MenteeEducation.objects.filter(mentee=mentee)

            raise rest_exceptions.PermissionDenied('You cannot view the education list of the requested mentee.')

        elif self.request.user.is_mentee:
            if self.request.user == mentee.user:
                return MenteeEducation.objects.filter(mentee=mentee)

            raise rest_exceptions.PermissionDenied('You cannot view the education list of the requested mentee.')

    def list(self, request, *args, **kwargs):
        """
        This function validates and returns list depending upon whether the requesting user is a mentor or a mentee.
        The validation checks and filtering is done in overridden get_queryset() method.
        """

        if 'mentee' not in request.query_params:
            return Response(data=dict(mentee='You should provide the `mentee` query parameter.'),
                            status=status.HTTP_400_BAD_REQUEST)

        if not Mentee.objects.filter(uid=request.query_params['mentee']).exists():
            return Response(data=dict(mentee='Invalid mentee UID provided.'), status=status.HTTP_400_BAD_REQUEST)

        return super().list(request, *args, **kwargs)


class MenteeResearchViewSet(ViewSetPermissionByMethodMixin, viewsets.ModelViewSet):
    permission_classes = (mentee_permissions.CanAccessMenteeResearch,)
    permission_action_classes = dict(
        create=(mentee_permissions.IsMentee,),
        retrieve=(mentee_permissions.CanRetrieveMenteeResearch,),
        list=(permissions.IsAuthenticated,)
    )
    serializer_class = MenteeResearchSerializer
    queryset = MenteeResearch.objects.all()
    lookup_field = 'uid'

    def get_queryset(self):
        if self.action != 'list':
            return super().get_queryset()

        mentee = Mentee.objects.get(uid=self.request.query_params['mentee'])
        if self.request.user.is_mentor:
            if mentee_permissions.CanRetrieveMentee().has_object_permission(self.request, self, mentee):
                return MenteeResearch.objects.filter(mentee=mentee)

            raise rest_exceptions.PermissionDenied('You cannot view the education list of the requested mentee.')

        elif self.request.user.is_mentee:
            if self.request.user == mentee.user:
                return MenteeResearch.objects.filter(mentee=mentee)

            raise rest_exceptions.PermissionDenied('You cannot view the education list of the requested mentee.')

    def list(self, request, *args, **kwargs):
        """
        This function validates and returns list depending upon whether the requesting user is a mentor or a mentee.
        The validation checks and filtering is done in overridden get_queryset() method.
        """

        if 'mentee' not in request.query_params:
            return Response(data=dict(mentee='You should provide the `mentee` query parameter.'),
                            status=status.HTTP_400_BAD_REQUEST)

        if not Mentee.objects.filter(uid=request.query_params['mentee']).exists():
            return Response(data=dict(mentee='Invalid mentee UID provided.'), status=status.HTTP_400_BAD_REQUEST)

        return super().list(request, *args, **kwargs)
