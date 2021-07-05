import uuid

from django.db import models


class MentorshipRequestStatus(models.IntegerChoices):
    REQUEST_PENDING = (1, 'Request pending')
    REQUEST_ACCEPTED = (2, 'Request accepted')
    REQUEST_REJECTED = (3, 'Request rejected')


class MentorshipStatus(models.IntegerChoices):
    ONGOING = (1, 'Ongoing')
    FINISHED = (2, 'Finished')
    TERMINATED = (3, 'Terminated')


class Mentorship(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentor = models.ForeignKey('mentor.Mentor', on_delete=models.CASCADE,
                               related_name='mentor_mentorships')  # TODO Give better and smaller related_name
    mentee = models.ForeignKey('mentee.Mentee', on_delete=models.CASCADE, related_name='mentee_mentorships')
    status = models.IntegerField(choices=MentorshipStatus.choices, default=MentorshipStatus.ONGOING)
    start_date = models.DateField(verbose_name='Start date', auto_now_add=True)  # TODO [V] Max value = today
    end_date = models.DateField(verbose_name='End date',
                                null=True)  # When the mentor-mentee relationship actually ended
    expected_end_date = models.DateField(verbose_name='Expected end date', null=True,
                                         blank=True)  # TODO [V] Min value > start_date, default value should be as per the mentor's preference

    # TODO Save MentorshipRequest upon acceptance?

    def __str__(self):
        return '{}(mentor={}, mentee={})'.format(self.__class__.__name__,
                                                 self.mentor.user.email,
                                                 self.mentee.user.email)


class MentorshipRequest(models.Model):  # TODO Change fields, give better names, make more organized and comprehensible
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentor = models.ForeignKey('mentor.Mentor', on_delete=models.CASCADE)
    mentee = models.ForeignKey('mentee.Mentee', on_delete=models.CASCADE)

    statement_of_purpose = models.TextField(max_length=512, blank=True)
    expectations = models.TextField(max_length=256, blank=True)
    commitment = models.TextField(max_length=256, blank=True)
    status = models.IntegerField(choices=MentorshipRequestStatus.choices,
                                 default=MentorshipRequestStatus.REQUEST_PENDING)
    reject_reason = models.TextField(max_length=256, blank=True)  # Only if status is request_rejected

    date = models.DateField(auto_now_add=True, editable=False)

    def __str__(self):
        return '{}(mentor={}, mentee={})'.format(self.__class__.__name__,
                                                 self.mentor.user.email,
                                                 self.mentee.user.email)


class Meeting(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentorship = models.ForeignKey('mentorship.Mentorship', on_delete=models.CASCADE, related_name='meetings')
    creator = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='meetings_created')

    title = models.CharField(max_length=64, blank=False)
    agenda = models.CharField(max_length=128, blank=True)
    date_time = models.DateTimeField(auto_now_add=False)
    url = models.URLField(blank=True)

    def __str__(self):
        return '{}(mentor={}, mentee={})'.format(self.__class__.__name__,
                                                 self.mentorship.mentor.user.email,
                                                 self.mentorship.mentee.user.email)


class MeetingSummary(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    meeting = models.OneToOneField('mentorship.Meeting', on_delete=models.CASCADE, related_name='summary')

    date_time = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    description = models.TextField(max_length=512, blank=True)
    todos = models.TextField(max_length=512, blank=True)

    next_meeting_date = models.DateTimeField(auto_now_add=False)
    next_meeting_agenda = models.TextField(max_length=512, blank=True)

    class Meta:
        verbose_name_plural = 'MeetingSummaries'

    def __str__(self):
        return "{}(mentor={}, mentee={})".format(self.__class__.__name__,
                                                 self.meeting.mentorship.mentor.user.email,
                                                 self.meeting.mentorship.mentee.user.email)


class Milestone(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    mentorship = models.ForeignKey('mentorship.Mentorship', on_delete=models.CASCADE, related_name='milestones')
    date = models.DateField(auto_now_add=True)
    description = models.TextField(max_length=256)

    def __str__(self):
        return "{}(mentor={}, mentee={}, date={})".format(self.__class__.__name__,
                                                          self.mentorship.mentor.user.email,
                                                          self.mentorship.mentee.user.email,
                                                          self.date)

# TODO Add class DeletedMentorMenteeRelation(models.Model)
