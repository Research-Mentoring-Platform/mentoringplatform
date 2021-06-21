from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers

from mentee.models import Mentee
from mentor.models import Mentor
from mentorship.models import MentorshipRequest, MentorshipRequestStatus, Mentorship


class MentorshipSerializer(serializers.ModelSerializer):
    mentor = serializers.SlugRelatedField(slug_field='uid',
                                          read_only=True)

    mentee = serializers.SlugRelatedField(slug_field='uid',
                                          read_only=True)


class MentorshipRequestSerializer(serializers.ModelSerializer):
    mentor = serializers.SlugRelatedField(slug_field='uid',
                                          queryset=Mentor.objects.all(),
                                          read_only=False,
                                          required=True,
                                          allow_null=False)

    mentee = serializers.SlugRelatedField(slug_field='uid',
                                          queryset=Mentee.objects.all(),
                                          read_only=False,
                                          required=True,
                                          allow_null=False)

    class Meta:
        model = MentorshipRequest
        exclude = ('id',)
        read_only_fields = ('uid', 'status', 'reject_reason', 'date')


class MentorshipRequestAcceptanceSerializer(serializers.ModelSerializer):
    accepted = serializers.BooleanField(required=True)

    class Meta:
        model = MentorshipRequest
        fields = ('accepted', 'reject_reason')

    def validate(self, attrs):
        data = super().validate(attrs)
        if not data['accepted'] and attrs['reject_reason'] == '':
            raise rest_exceptions.ValidationError('Provide a reject_reason for rejection.')
        if data['accepted'] and attrs['reject_reason'] != '':
            raise rest_exceptions.ValidationError('Reject reason not needed for acceptance.')
        return data

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        if validated_data['accepted']:
            instance.status = MentorshipRequestStatus.REQUEST_ACCEPTED
            Mentorship.objects.create(mentor=instance.mentor, mentee=instance.mentee)
        else:
            instance.status = MentorshipRequestStatus.REQUEST_REJECTED
            instance.reject_reason = validated_data['reject_reason']
        instance.save()
        return instance
