import uuid

from django.db import models


# TODO can be completely removed. Only kept for record-keeping.
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
    start_date = models.DateField(verbose_name='Start date', auto_now_add=True)
    end_date = models.DateField(verbose_name='End date', blank=True,
                                null=True)  # When the mentor-mentee relationship actually ended
    expected_end_date = models.DateField(verbose_name='Expected end date', null=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return '{}(mentor={}, mentee={})'.format(self.__class__.__name__,
                                                 self.mentor.user.email,
                                                 self.mentee.user.email)


class MentorshipRequest(models.Model):  # TODO Change fields, give better names, make more organized and comprehensible
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentor = models.ForeignKey('mentor.Mentor', on_delete=models.CASCADE, related_name='mentor_mentorship_requests')
    mentee = models.ForeignKey('mentee.Mentee', on_delete=models.CASCADE, related_name='mentee_mentorship_requests')

    statement_of_purpose = models.TextField(max_length=512, blank=True)
    expectations = models.TextField(max_length=256, blank=True)
    commitment = models.TextField(max_length=256, blank=True)
    status = models.IntegerField(choices=MentorshipRequestStatus.choices,
                                 default=MentorshipRequestStatus.REQUEST_PENDING)
    reject_reason = models.TextField(max_length=256, blank=True)  # Only if status is request_rejected

    date = models.DateField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['-date']

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

    class Meta:
        ordering = ['date_time']

    def __str__(self):
        return '{}(mentor={}, mentee={})'.format(self.__class__.__name__,
                                                 self.mentorship.mentor.user.email,
                                                 self.mentorship.mentee.user.email)


class MeetingSummary(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    meeting = models.OneToOneField('mentorship.Meeting', on_delete=models.CASCADE, related_name='summary')

    date_time = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(null=True, blank=True)  # Number of hours (e.g. 1, 1.5 etc)
    description = models.TextField(max_length=512, blank=True)
    todos = models.TextField(max_length=512, blank=True)

    next_meeting_date_time = models.DateTimeField(auto_now_add=False)
    next_meeting_agenda = models.TextField(max_length=512, blank=True)

    class Meta:
        # ordering = ['date_time']
        verbose_name_plural = 'MeetingSummaries'

    def __str__(self):
        return "{}(mentor={}, mentee={})".format(self.__class__.__name__,
                                                 self.meeting.mentorship.mentor.user.email,
                                                 self.meeting.mentorship.mentee.user.email)


class Milestone(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentorship = models.ForeignKey('mentorship.Mentorship', on_delete=models.CASCADE, related_name='milestones')

    title = models.CharField(max_length=64)
    date = models.DateField()
    description = models.TextField(max_length=256)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return "{}(mentor={}, mentee={}, title={})".format(self.__class__.__name__,
                                                           self.mentorship.mentor.user.email,
                                                           self.mentorship.mentee.user.email,
                                                           self.title)

# TODO Add class DeletedMentorMenteeRelation(models.Model)
