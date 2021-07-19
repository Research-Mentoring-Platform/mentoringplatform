import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainSlidingSerializer

from users.methods import verify_login, invalidate_old_authentication_token
from users.models import CustomUser, ForgotPasswordToken


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )

    class Meta:
        model = get_user_model()
        fields = ('uid', 'first_name', 'last_name', 'email', 'username', 'password', 'date_of_birth',
                  'is_mentor', 'is_mentee')  # this restricts API users from creating an admin
        read_only_fields = ('uid',)

    def validate(self, attrs):
        data = super().validate(attrs)
        errors = dict()

        if data['is_mentor'] == data['is_mentee']:
            errors['non_field_errors'] = 'You can be either mentor or mentee.'

        if (datetime.date.today() - data['date_of_birth']) <= datetime.timedelta(days=13 * 365):
            errors['date_of_birth'] = 'You must be at least 13 years old to register on this platform.'

        if len(errors) > 0:
            raise rest_exceptions.ValidationError(errors)

        return data

    #  https://stackoverflow.com/a/27586289/5394180
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        raise rest_exceptions.PermissionDenied('Updation not allowed.')


# https://stackoverflow.com/a/22133032/5394180
class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta(CustomUserSerializer.Meta):
        model = get_user_model()
        fields = ('uid', 'first_name', 'last_name')
        read_only_fields = ('uid',)

    def create(self, validated_data):
        raise rest_exceptions.PermissionDenied('Creation not allowed.')


class CustomUserPasswordUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('current_password', 'new_password',)

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.context['request'].user
        if not user.check_password(data['current_password']):
            raise rest_exceptions.ValidationError(dict(current_password='Invalid current password'))

        if data['current_password'] == data['new_password']:
            raise rest_exceptions.ValidationError(dict(new_password='New password cannot be the same as the '
                                                                    'previous password.'))

        try:
            validate_password(data['new_password'])
            return data
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(dict(new_password='\n'.join(e.messages)))

    def create(self, validated_data):
        raise rest_exceptions.PermissionDenied('Creation not allowed.')

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        invalidate_old_authentication_token(instance)
        return instance


# https://stackoverflow.com/a/55859751/5394180
class CustomTokenObtainSlidingSerializer(TokenObtainSlidingSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # this must be the first line (self.user initiates in super().validate())
        verify_login(self.user)
        data['uid'] = self.user.uid
        data['profile_uid'] = self.user.mentor.uid if self.user.is_mentor else self.user.mentee.uid
        return data


class CustomUserForgotPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('token', 'new_password',)

    def validate(self, attrs):
        data = super().validate(attrs)
        token = ForgotPasswordToken.objects.filter(token=data['token'])
        if not token.exists():
            raise rest_exceptions.ValidationError(dict(token='Invalid token'))

        token = token.first()
        if token.is_expired:
            raise rest_exceptions.ValidationError(dict(token='Token expired. Generate a new one.'))

        if token.user.check_password(data['new_password']):
            raise rest_exceptions.ValidationError(dict(new_password='New password cannot be the same as the '
                                                                    'previous password.'))

        try:
            validate_password(data['new_password'])
            return data
        except django_exceptions.ValidationError as e:
            raise rest_exceptions.ValidationError(dict(new_password='\n'.join(e.messages)))


class CustomUserForgotPasswordTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise rest_exceptions.ValidationError(dict(email='No user with given email exists.'))

        return value
