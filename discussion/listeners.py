from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

notification = None
if 'notification' in settings.INSTALLED_APPS:
    from notification import models as notification

from .models import Comment, Post


@receiver(post_save, sender=Post)
def post_notifications(sender, created, **kwargs):
    if notification and created:
        # what users to send to?
        # notification.send([to_user], 'discussion_post_save', {'from_user': from_user})
        pass


@receiver(post_save, sender=Comment)
def comment_notifications(sender, created, **kwargs):
    if notification and created:
        pass

