from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


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
        instance.set_password(validated_data.pop('password'))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# https://stackoverflow.com/a/22133032/5394180
class CustomUserUpdateSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        fields = ('uid', 'first_name', 'last_name')
