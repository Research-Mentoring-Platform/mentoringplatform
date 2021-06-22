from datetime import datetime

from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers

from mentee.models import Mentee
from mentor.models import Mentor
from mentorship.models import MentorshipRequest, MentorshipRequestStatus, Mentorship, MentorshipStatus, Meeting, \
    MeetingSummary
from users.models import CustomUser


class MentorshipSerializer(serializers.ModelSerializer):
    mentor = serializers.SlugRelatedField(slug_field='uid',
                                          read_only=True)

    mentee = serializers.SlugRelatedField(slug_field='uid',
                                          read_only=True)

    class Meta:
        model = Mentorship
        exclude = ('id',)
        read_only_fields = ('uid', 'start_date', 'end_date')  # Mentor and Mentee are already set to read_only

    def create(self, validated_data):
        # TODO will this ever be called?
        pass

    def validate(self, attrs):
        data = super().validate(attrs)
        if 'status' in data:  # status is an optional field to update
            if data['status'] == MentorshipStatus.ONGOING:
                raise rest_exceptions.ValidationError('Mentorship status cannot be updated to ongoing')
        return data

    def update(self, instance, validated_data):
        # Change end_date if status is updated
        if 'status' in validated_data:  # status is an optional field
            instance.end_date = datetime.now()  # Mentorship ended, update end time

        for field in validated_data:
            setattr(instance, field, validated_data[field])

        instance.save()
        return instance


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


class MeetingSerializer(serializers.ModelSerializer):
    mentorship = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=Mentorship.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    creator = serializers.SlugRelatedField(slug_field='uid',
                                           queryset=CustomUser.objects.all(),
                                           read_only=False,
                                           required=True,
                                           allow_null=False)

    class Meta:
        model = Meeting
        exclude = ('id',)


class MeetingSummarySerializer(serializers.ModelSerializer):
    meeting = serializers.SlugRelatedField(slug_field='uid',
                                           read_only=True,
                                           required=True,
                                           allow_null=False)

    class Meta:
        model = MeetingSummary
        exclude = ('uid',)
