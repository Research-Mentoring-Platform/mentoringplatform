from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers

from mentee.models import MenteeDesignation
from mentor.models import Mentor, MentorDesignation, MentorDepartment, MentorDiscipline, MentorResponsibility, \
    MentorEducation, MentorResearch


class MentorSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='uid',
                                        read_only=True)

    designation = serializers.SlugRelatedField(slug_field='uid',
                                               queryset=MentorDesignation.objects.all(),
                                               read_only=False,
                                               required=True,
                                               allow_null=False)

    department = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MentorDepartment.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    discipline = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=MentorDiscipline.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    accepted_mentee_types = serializers.SlugRelatedField(slug_field='uid',
                                                         queryset=MenteeDesignation.objects.all(),
                                                         read_only=False,
                                                         many=True,
                                                         required=False,
                                                         allow_null=True)
    responsibilities = serializers.SlugRelatedField(slug_field='uid',
                                                    queryset=MentorResponsibility.objects.all(),
                                                    read_only=False,
                                                    many=True,
                                                    required=False,
                                                    allow_null=True)

    class Meta:
        model = Mentor
        exclude = ('id',)
        read_only_fields = ('uid', 'rating', 'profile_completed', 'is_verified', 'user')


class MentorResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorResponsibility
        exclude = ('id',)
        read_only_fields = ('uid', 'description',)


class MentorDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorDepartment
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MentorDesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorDesignation
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MentorDisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorDiscipline
        exclude = ('id',)
        read_only_fields = ('uid', 'label',)


class MentorEducationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m')
    end_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m', allow_null=True)
    mentor = serializers.SlugRelatedField(slug_field='uid',
                                          queryset=Mentor.objects.all(),
                                          read_only=False,
                                          required=True,
                                          allow_null=False)

    class Meta:
        model = MentorEducation
        fields = '__all__'
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.context['request'].user != attrs['mentor'].user:
            raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='It must not be later than the end date.',
                                                           end_date='It must not be earlier than the start date.', ))

        return data


class MentorResearchSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m')
    end_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m', allow_null=True)
    mentor = serializers.SlugRelatedField(slug_field='uid',
                                          queryset=Mentor.objects.all(),
                                          read_only=False,
                                          required=True,
                                          allow_null=False)

    class Meta:
        model = MentorResearch
        fields = '__all__'
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.context['request'].user != attrs['mentor'].user:
            raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='It must not be later than the end date.',
                                                           end_date='It must not be earlier than the start date.', ))

        return data
