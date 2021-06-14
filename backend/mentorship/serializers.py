from django.contrib.auth import get_user_model
from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers

from mentorship.models import Education


class EducationSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m')
    end_date = serializers.DateField(input_formats=('%Y-%m',), format='%Y-%m', allow_null=True)
    user = serializers.SlugRelatedField(slug_field='uid',
                                        queryset=get_user_model().objects.all(),
                                        read_only=False,
                                        required=True,
                                        allow_null=False)

    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        if self.context['request'].user.uid != attrs['user'].uid:
            raise rest_exceptions.PermissionDenied(dict(user='Incorrect User UID provided.'))
        return data
