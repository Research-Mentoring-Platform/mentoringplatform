import uuid

from django.db import models


class Mentor(models.Model):  # TODO: Rename Mentor to MentorProfile?
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    profile_completed = models.BooleanField(default=False)
    about_self = models.TextField(max_length=512, blank=True)

    designation = models.ForeignKey('mentor.MentorDesignation', on_delete=models.RESTRICT,
                                    related_name='mentors_with_designation',
                                    null=True)
    department = models.ForeignKey('mentor.MentorDepartment', on_delete=models.RESTRICT,
                                   related_name='mentors_with_department',
                                   null=True)
    discipline = models.ForeignKey('mentor.MentorDiscipline', on_delete=models.RESTRICT,
                                   related_name='mentors_with_discipline',
                                   null=True)
    specialization = models.TextField(max_length=256, blank=True)
    # Additional fields: Education, Research

    expected_min_mentorship_duration = models.DurationField(null=True,
                                                            blank=True)  # 1 month / 2 month / No min duration
    expected_max_mentorship_duration = models.DurationField(null=True,
                                                            blank=True)  # 3 month / 4 month / No max duration
    is_accepting_mentorship_requests = models.BooleanField(default=True)

    accepted_mentee_types = models.ManyToManyField('mentee.MenteeDesignation')
    responsibilities = models.ManyToManyField('mentor.MentorResponsibility')
    other_responsibility = models.TextField(max_length=512, blank=True)

    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True,
                                 # validators=[validators.MinValueValidator(0.0), validators.MaxValueValidator(5.0)]
                                 )  # TODO Check if validators can be added here or only in DRF Serializers
    # TODO rating must keep track of who rated whom

    # TODO Add social_handles

    def __str__(self):
        return '{}(email={}, verified={})'.format(self.__class__.__name__,
                                                  self.user.email,
                                                  self.is_verified)


class MentorResponsibility(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    description = models.TextField(max_length=256, blank=False)

    def __str__(self):
        return '{}(description={})'.format(self.__class__.__name__, self.description)


class MentorDepartment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)


class MentorDesignation(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return '{}(email={})'.format(self.__class__.__name__, self.label)


class MentorDiscipline(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)


class MentorEducation(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # TODO convertable to GenericForeignKey to either of Mentee and Mentor models (
    #  https://bhrigu.medium.com/django-how-to-add-foreignkey-to-multiple-models-394596f06e84)
    mentor = models.ForeignKey('mentor.Mentor', on_delete=models.CASCADE, related_name='educations')

    qualification = models.CharField(max_length=128, blank=False)
    organization = models.CharField(max_length=128, blank=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)  # null == True signifies ongoing
    details = models.TextField(max_length=512, blank=True)  # TODO Convert to RichTextField

    def __str__(self):
        return '{}(email={}, qualification={})'.format(self.__class__.__name__, self.mentor.user.email,
                                                       self.qualification)


class MentorResearch(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentor = models.ForeignKey('mentor.Mentor', on_delete=models.CASCADE, related_name='researches')

    title = models.CharField(max_length=128, blank=False)
    organization = models.CharField(max_length=128, blank=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)  # null == True signifies ongoing
    details = models.TextField(max_length=512, blank=True)

    def __str__(self):
        return '{}(email={}, title={})'.format(self.__class__.__name__, self.mentor.user.email, self.title)
