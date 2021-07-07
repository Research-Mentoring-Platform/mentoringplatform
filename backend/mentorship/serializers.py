from rest_framework import exceptions as rest_exceptions
from rest_framework import serializers

from mentee.models import Mentee
from mentor.models import Mentor
from mentorship.models import MentorshipRequest, MentorshipRequestStatus, Mentorship, MentorshipStatus, Meeting, \
    MeetingSummary, Milestone
from users.models import CustomUser


class MentorshipSerializer(serializers.ModelSerializer):
    mentor = serializers.SlugRelatedField(slug_field='uid',
                                          read_only=True)

    mentee = serializers.SlugRelatedField(slug_field='uid',
                                          read_only=True)

    class Meta:
        model = Mentorship
        exclude = ('id',)
        read_only_fields = (
        'uid', 'mentor', 'mentee', 'start_date', 'end_date', 'status')  # Mentor and Mentee are already set to read_only

    def create(self, validated_data):
        raise rest_exceptions.PermissionDenied('Direct creation not allowed.')

    def validate(self, attrs):
        data = super().validate(attrs)

        # TODO Check if expected_end_date is always in request
        if data['expected_end_date'] < self.instance.start_date:
            raise rest_exceptions.ValidationError(dict(expected_end_date='Expected end date cannot be earlier '
                                                                         'than the start date'))

        return data


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

    def validate(self, attrs):  # only for creation
        data = super().validate(attrs)

        if not attrs['mentor'].is_verified:
            raise rest_exceptions.ValidationError('The specified mentor is unverified by the admins.')

        if Mentorship.objects.filter(mentor=attrs['mentor'], mentee=attrs['mentee'],
                                     status=MentorshipStatus.ONGOING).exists():
            raise rest_exceptions.ValidationError('There is an ongoing mentorship between the specified mentor and '
                                                  'mentee.')

        if MentorshipRequest.objects.filter(mentor=attrs['mentor'], mentee=attrs['mentee'],
                                            status=MentorshipRequestStatus.REQUEST_PENDING).exists():
            raise rest_exceptions.ValidationError('A mentorship request between the specified mentor and mentee is '
                                                  'pending.')

        return data


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
        raise rest_exceptions.PermissionDenied('Direct creation not allowed.')

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

    def update(self, instance, validated_data):
        validated_data.pop('creator')  # Make sure creator is not changed after creation
        validated_data.pop('mentorship')  # Cannot reassign meeting to another mentorship
        return super().update(instance, validated_data)

    def validate_creator(self, value):
        if self.context['request'].user == value:  # Creator is part of the mentorship is checked in validate_mentorship
            return value

        # TODO Change import statement from rest_exceptions to serializers
        raise rest_exceptions.PermissionDenied('You can only create your own meetings')

    def validate_mentorship(self, value):
        if (self.context['request'].user == value.mentorship.mentor.user) or \
                (self.context['request'].user == value.mentorship.mentee.user):
            return value

        raise rest_exceptions.PermissionDenied('You are not a part of this mentorship\'s meetings.')


class MeetingSummarySerializer(serializers.ModelSerializer):
    meeting = serializers.SlugRelatedField(slug_field='uid',
                                           queryset=Meeting.objects.all(),
                                           read_only=False,
                                           required=True,
                                           allow_null=False)

    class Meta:
        model = MeetingSummary
        exclude = ('uid',)

    def update(self, instance, validated_data):
        validated_data.pop('meeting')  # Cannot reassign summary to another meeting
        return super().update(instance, validated_data)

    def validate_meeting(self, value):
        if (self.context['request'].user == value.meeting.mentorship.mentor.user) or \
                (self.context['request'].user == value.meeting.mentorship.mentee.user):
            return value

        return rest_exceptions.PermissionDenied('You are not a part of this mentorship\'s meeting summaries.')


class MilestoneSerializer(serializers.ModelSerializer):
    mentorship = serializers.SlugRelatedField(slug_field='uid',
                                              queryset=Mentorship.objects.all(),
                                              read_only=False,
                                              required=True,
                                              allow_null=False)

    class Meta:
        model = Milestone
        exclude = ('id',)

    def update(self, instance, validated_data):
        validated_data.pop('mentorship')  # Cannot reassign milestone to another mentorship
        return super().update(instance, validated_data)

    def validate_mentorship(self, value):
        if (self.context['request'].user == value.mentorship.mentor.user) or \
                (self.context['request'].user == value.mentorship.mentee.user):
            return value

        return rest_exceptions.PermissionDenied('You are not a part of this mentorship\'s milestones.')
