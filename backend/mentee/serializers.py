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
        fields = ('uid', 'user', 'about_self', 'profile_completed',
                  'designation', 'department', 'discipline', 'specialization', 'rating')
        read_only_fields = ('uid', 'rating', 'profile_completed')  # user is already read-only

    def validate(self, attrs):
        data = super().validate(attrs)
        if 'rating' in data:
            raise rest_exceptions.PermissionDenied("Rating is a restricted field and cannot be updated.")


class MenteeViewSerializer(MenteeSerializer):
    first_name = serializers.SerializerMethodField(method_name='get_first_name', read_only=True)
    last_name = serializers.SerializerMethodField(method_name='get_last_name', read_only=True)
    username = serializers.SerializerMethodField(method_name='get_username', read_only=True)
    designation_label = serializers.SerializerMethodField(method_name='get_designation_label', read_only=True)
    department_label = serializers.SerializerMethodField(method_name='get_department_label', read_only=True)
    discipline_label = serializers.SerializerMethodField(method_name='get_discipline_label', read_only=True)

    class Meta(MenteeSerializer.Meta):
        fields = MenteeSerializer.Meta.fields + ('first_name',
                                                 'last_name',
                                                 'username',
                                                 'designation_label',
                                                 'department_label',
                                                 'discipline_label')

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

    def create(self, validated_data):
        raise rest_exceptions.PermissionDenied('Invalid request.')

    def update(self, instance, validated_data):
        raise rest_exceptions.PermissionDenied('Invalid request.')


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
        if 'mentee' in data:
            if self.context['request'].user != data['mentee'].user:
                raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='Start date must not be later than the end date.',
                                                           end_date='End date must not be earlier than the start date.', ))

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
        if 'mentee' in data:
            if self.context['request'].user != data['mentee'].user:
                raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise rest_exceptions.ValidationError(dict(start_date='It must not be later than the end date.',
                                                           end_date='It must not be earlier than the start date.', ))

        return data
