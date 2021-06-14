from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from mentee.models import Mentee
from mentor.models import Mentor
from users.models import CustomUser


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
                  'is_mentor', 'is_mentee')
        read_only_fields = ('uid',)

    def validate(self, attrs):
        if attrs['is_mentor'] == attrs['is_mentee']:
            raise serializers.ValidationError('You can be either mentor or mentee.')
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
        raise NotImplementedError('Do not allow updates.')  # TODO is raising this a good idea? (500 server error)


# https://stackoverflow.com/a/22133032/5394180
class CustomUserUpdateSerializer(serializers.ModelSerializer):
    class Meta(CustomUserSerializer.Meta):
        model = get_user_model()
        fields = ('uid', 'first_name', 'last_name')
        read_only_fields = ('uid',)

    def create(self, validated_data):
        raise NotImplementedError('Do not allow creation.')  # TODO is raising this a good idea? (500 server error)


class CustomUserPasswordUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('current_password', 'new_password',)

    def validate(self, attrs):
        user = self.context['request'].user
        if user.check_password(attrs['current_password']):
            if user.check_password(attrs['new_password']):
                raise rest_exceptions.ValidationError(dict(new_password='New password cannot be the same as the '
                                                                        'previous password.'))
            try:
                validate_password(attrs['new_password'])
                return attrs
            except django_exceptions.ValidationError as e:
                raise rest_exceptions.ValidationError(dict(new_password=' '.join(e.messages)))

        raise rest_exceptions.ValidationError(dict(current_password='Invalid current password'))

    def create(self, validated_data):
        raise NotImplementedError('Do not allow creation.')  # TODO is raising this a good idea? (500 server error)

    def update(self, instance, validated_data):
        instance.set_password(
            validated_data['new_password'])  # TODO how to invalidate the existing tokens before expiry?
        instance.save()
        return instance


# https://stackoverflow.com/a/55859751/5394180
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)  # this must be the first line (self.user initiates in super().validate())

        if self.user.is_admin and (not self.user.is_mentor):
            raise rest_exceptions.ValidationError('Non-mentor admins should use backend admin-login instead')

        if not self.user.email_verified:
            raise rest_exceptions.ValidationError('Email not verified.')

        data['user_uid'] = self.user.uid

        if self.user.is_mentor:
            if not hasattr(self.user, 'mentor'):
                Mentor.objects.create(user=self.user)

            data['profile_uid'] = self.user.mentor.uid

        else:  # is mentee
            if not hasattr(self.user, 'mentee'):
                Mentee.objects.create(user=self.user)

            data['profile_uid'] = self.user.mentee.uid

        return data


class CustomUserEmailVerificationSerializer(serializers.Serializer):
    email_verification_token = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        email_verification_token = data['email_verification_token']
        user = CustomUser.objects.get(email_verification_token=email_verification_token)
