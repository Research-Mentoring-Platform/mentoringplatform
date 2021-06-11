from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from mentee.models import Mentee
from mentor.models import Mentor


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created=False, **kwargs):
    user = instance
    if created:
        if user.is_mentee:
            Mentee.objects.create(user=user)
        elif user.is_mentor:
            Mentor.objects.create(user=user)
