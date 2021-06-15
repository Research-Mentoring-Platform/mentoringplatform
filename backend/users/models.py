import uuid

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.core.exceptions import ValidationError
from django.db import models

from users.methods import generate_email_verification_token


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, date_of_birth, password=None,
                    is_mentor=False, is_mentee=False, is_admin=False):
        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          username=username,
                          date_of_birth=date_of_birth,
                          is_mentor=is_mentor,
                          is_mentee=is_mentee,
                          is_admin=is_admin)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, username, date_of_birth, password=None):
        return self.create_user(email=email,
                                first_name=first_name,
                                last_name=last_name,
                                username=username,
                                password=password,
                                date_of_birth=date_of_birth,
                                is_mentor=False,
                                is_mentee=False,
                                is_admin=True)


class CustomUser(AbstractBaseUser):
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    email = models.EmailField(verbose_name='Email address', unique=True, max_length=48)
    username = models.CharField(verbose_name='Username', unique=True, max_length=16, blank=False)
    first_name = models.CharField(verbose_name='First name', max_length=20, blank=False)
    last_name = models.CharField(verbose_name='Last name', max_length=20, blank=False)
    date_of_birth = models.DateField(verbose_name='Date of birth')
    is_mentor = models.BooleanField(verbose_name='Is mentor?', default=False, blank=True)
    is_mentee = models.BooleanField(verbose_name='Is mentee?', default=False, blank=True)

    # To be set in back-end (not shown in registration form)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(verbose_name='Is admin?', default=False)
    email_verified = models.BooleanField(verbose_name='Email verified?', default=False)
    email_verification_token = models.CharField(max_length=32, default=generate_email_verification_token)

    # Django-specific fields
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'date_of_birth']

    def clean(self):
        if self.is_admin and self.is_mentee:
            raise ValidationError('A mentee cannot be an admin')

        if self.is_mentor and self.is_mentee:
            raise ValidationError('A user cannot be both a mentor and a mentee')

        return super().clean()

    # https://stackoverflow.com/questions/18803112/django-doesnt-call-model-clean-method
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}(email={})'.format(self.__class__.__name__, self.email)

    def has_perm(self, perm, obj=None):  # TODO Check
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def is_staff(self):
        return self.is_admin

    # https://stackoverflow.com/a/22027915/5394180
    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def full_name(self):
        return self.get_full_name()
