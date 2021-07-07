import uuid

from django.db import models
from django.db.models import F


class Mentee(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)

    about_self = models.TextField(max_length=512, blank=True)  # TODO add field for CV/resume
    profile_completed = models.BooleanField(default=False)
    designation = models.ForeignKey('mentee.MenteeDesignation', on_delete=models.RESTRICT,
                                    related_name='mentees_with_designation',
                                    null=True)
    department = models.ForeignKey('mentee.MenteeDepartment', on_delete=models.RESTRICT,
                                   related_name='mentees_with_department',
                                   null=True)
    discipline = models.ForeignKey('mentee.MenteeDiscipline', on_delete=models.RESTRICT,
                                   related_name='mentees_with_discipline',
                                   null=True)
    specialization = models.TextField(max_length=256, blank=True)
    # Additional fields: Education, Research

    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True
                                 # validators=[validators.MinValueValidator(0.0), validators.MaxValueValidator(5.0)]
                                 )  # TODO Check if validators can be added here or only in DRF Serializers

    # TODO rating must keep track of who rated whom

    def __str__(self):
        return '{}(email={})'.format(self.__class__.__name__, self.user.email)


class MenteeDesignation(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    label = models.CharField(max_length=32, blank=False, unique=True)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)


class MenteeDepartment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    label = models.CharField(max_length=32, blank=False, unique=True)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)


class MenteeDiscipline(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    label = models.CharField(max_length=32, blank=False, unique=True)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)


class MenteeEducation(models.Model):
    # TODO convertable to GenericForeignKey to either of Mentee and Mentee models (
    #  https://bhrigu.medium.com/django-how-to-add-foreignkey-to-multiple-models-394596f06e84)
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentee = models.ForeignKey('mentee.Mentee', on_delete=models.CASCADE, related_name='educations')

    qualification = models.CharField(max_length=128, blank=False)
    organization = models.CharField(max_length=128, blank=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)  # null == True signifies ongoing
    details = models.TextField(max_length=512, blank=True)  # TODO Convert to RichTextField
    link = models.URLField(blank=True)

    class Meta:
        ordering = [F('end_date').desc(nulls_last=True), '-start_date']

    def __str__(self):
        return '{}(email={}, qualification={})'.format(self.__class__.__name__, self.mentee.user.email,
                                                       self.qualification)


class MenteeResearch(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    mentee = models.ForeignKey('mentee.Mentee', on_delete=models.CASCADE, related_name='researches')

    title = models.CharField(max_length=128, blank=False)
    organization = models.CharField(max_length=128, blank=False)
    start_date = models.DateField()
    end_date = models.DateField(null=True)  # null == True signifies ongoing
    details = models.TextField(max_length=512, blank=True)

    class Meta:
        verbose_name_plural = 'MenteeResearches'
        ordering = [F('end_date').desc(nulls_last=True), '-start_date']

    def __str__(self):
        return '{}(email={}, title={})'.format(self.__class__.__name__, self.mentee.user.email, self.title)
