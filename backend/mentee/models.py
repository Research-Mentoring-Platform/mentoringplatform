import uuid

from django.db import models


class Mentee(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    about_self = models.TextField(max_length=512, blank=True)
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

    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True,
                                 # validators=[validators.MinValueValidator(0.0), validators.MaxValueValidator(5.0)]
                                 )  # TODO Check if validators can be added here or only in DRF Serializers

    # TODO rating must keep track of who rated whom

    def __str__(self):
        return '{}(email={})'.format(self.__class__.__name__, self.user.email)


class MenteeDesignation(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)


class MenteeDepartment(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)


class MenteeDiscipline(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    label = models.CharField(max_length=32, blank=False)

    def __str__(self):
        return '{}(label={})'.format(self.__class__.__name__, self.label)
