from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework import exceptions as rest_exceptions


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = (
            'uid', 'first_name', 'last_name', 'email', 'username', 'password', 'date_of_birth', 'is_mentor',
            'is_mentee')
        read_only_fields = ('uid',)

    def validate(self, attrs):
        if attrs['is_mentor'] and attrs['is_mentee']:
            raise serializers.ValidationError('You cannot be both a mentor and a mentee.')
        return attrs

    #  https://stackoverflow.com/a/27586289/5394180
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        validated_data.pop('password')  # Do not allow password to update from here
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# https://stackoverflow.com/a/22133032/5394180
class CustomUserUpdateSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        fields = ('uid', 'first_name', 'last_name')
        read_only_fields = ('uid',)


class CustomUserPasswordUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()

    def validate(self, attrs):
        user: get_user_model() = CurrentUserDefault()
        if user.check_password(attrs['current_password']):
            try:
                validate_password(attrs['new_password'])
            except django_exceptions.ValidationError as e:
                raise rest_exceptions.ValidationError(dict(new_password=e.message))
        raise rest_exceptions.ValidationError(dict(current_password='Invalid current password'))

    def update(self, instance, validated_data):  # TODO do we need to override create as well?
        instance.set_password(
            validated_data['new_password'])  # TODO how to invalidate the existing tokens before expiry?
        instance.save()
        return instance
