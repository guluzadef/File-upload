from django.db.models.signals import post_save
from django.dispatch import receiver
from base_user.models import MyUser

from .models import File, See


@receiver(post_save,sender=File)
def create_post(**kwargs):
    instance = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        See.objects.create(see_user=instance.user,see_file=instance,access_comment=True)