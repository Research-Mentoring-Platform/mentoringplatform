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
        fields = ('uid', 'user', 'is_verified',
                  'profile_completed', 'about_self', 'designation',
                  'department', 'discipline', 'specialization',
                  'expected_min_mentorship_duration', 'expected_max_mentorship_duration',
                  'is_accepting_mentorship_requests',
                  'accepted_mentee_types', 'responsibilities', 'other_responsibility',
                  'rating')  # TODO make it compact if possible
        read_only_fields = ('uid', 'rating', 'profile_completed', 'is_verified', 'user')

    def validate(self, attrs):
        data = super().validate(attrs)
        if 'rating' in data:
            raise rest_exceptions.PermissionDenied("Rating is a restricted field and cannot be updated.")


class MentorViewSerializer(MentorSerializer):
    first_name = serializers.SerializerMethodField(method_name='get_first_name', read_only=True)
    last_name = serializers.SerializerMethodField(method_name='get_last_name', read_only=True)
    username = serializers.SerializerMethodField(method_name='get_username', read_only=True)
    designation_label = serializers.SerializerMethodField(method_name='get_designation_label', read_only=True)
    department_label = serializers.SerializerMethodField(method_name='get_department_label', read_only=True)
    discipline_label = serializers.SerializerMethodField(method_name='get_discipline_label', read_only=True)
    accepted_mentee_type_labels = serializers.SerializerMethodField(method_name='get_accepted_mentee_type_labels',
                                                                    read_only=True)
    responsibility_descriptions = serializers.SerializerMethodField(method_name='get_responsibility_descriptions',
                                                                    read_only=True)

    class Meta(MentorSerializer.Meta):
        fields = MentorSerializer.Meta.fields + ('first_name',
                                                 'last_name',
                                                 'username',
                                                 'designation_label',
                                                 'department_label',
                                                 'discipline_label',
                                                 'accepted_mentee_type_labels',
                                                 'responsibility_descriptions')

    def get_first_name(self, instance):
        return instance.user.first_name

    def get_last_name(self, instance):
        return instance.user.last_name

    def get_username(self, instance):
        return instance.user.username

    def get_designation_label(self, instance):
        return getattr(instance.designation, 'label', None)

    def get_department_label(self, instance):
        return getattr(instance.department, 'label', None)

    def get_discipline_label(self, instance):
        return getattr(instance.discipline, 'label', None)

    def get_accepted_mentee_type_labels(self, instance):
        return [getattr(r, 'label', None) for r in instance.accepted_mentee_types.all()]

    def get_responsibility_descriptions(self, instance):
        return [getattr(r, 'description', None) for r in instance.responsibilities.all()]

    def create(self, validated_data):
        raise rest_exceptions.PermissionDenied('Invalid request.')

    def update(self, instance, validated_data):
        raise rest_exceptions.PermissionDenied('Invalid request.')


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
        exclude = ('id',)
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        if 'mentor' in data:
            if self.context['request'].user != data['mentor'].user:
                raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='Start date must not be later than the end date.',
                                                           end_date='End date not be earlier than the start date.', ))

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
        exclude = ('id',)
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        if 'mentor' in data:
            if self.context['request'].user != data['mentor'].user:
                raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='Start date must not be later than the end date.',
                                                           end_date='End date not be earlier than the start date.', ))

        return data
