from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers

from mentee.models import Mentee, MenteeDesignation, MenteeDepartment, MenteeDiscipline, MenteeEducation, MenteeResearch


class MenteeSerializer(serializers.ModelSerializer):
    # TODO add derived serializer for view-only access

    user = serializers.SlugRelatedField(slug_field='uid',
                                        read_only=True)
    designation = serializers.SlugRelatedField(slug_field='uid',
                                               queryset=MenteeDesignation.objects.all(),
                                               read_only=False,
                                               required=True,
                                               allow_null=False)
    department = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MenteeDepartment.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)
    discipline = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MenteeDiscipline.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    class Meta:
        model = Mentee
        exclude = ('id',)  # TODO should we exclude user from mentee-object response?
        read_only_fields = ('uid', 'rating', 'profile_completed')  # user is already read-only


class MenteeDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenteeDepartment
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MenteeDesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenteeDesignation
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MenteeDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenteeDiscipline
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MenteeEducationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m')
    end_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m', allow_null=True)
    mentee = serializers.SlugRelatedField(slug_field='uid',
                                          queryset=Mentee.objects.all(),
                                          read_only=False,
                                          required=True,
                                          allow_null=False)

    class Meta:
        model = MenteeEducation
        exclude = ('id',)
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.context['request'].user != attrs['mentee'].user:
            raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='It must not be later than the end date.',
                                                           end_date='It must not be earlier than the start date.', ))

        return data


class MenteeResearchSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m')
    end_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m', allow_null=True)
    mentee = serializers.SlugRelatedField(slug_field='uid',
                                          queryset=Mentee.objects.all(),
                                          read_only=False,
                                          required=True,
                                          allow_null=False)

    class Meta:
        model = MenteeResearch
        exclude = ('id',)
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.context['request'].user != attrs['mentee'].user:
            raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='It must not be later than the end date.',
                                                           end_date='It must not be earlier than the start date.', ))

        return data
