from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment, Post

if 'notification' in settings.INSTALLED_APPS:
    from notification import models as notification


    def post_notifications(sender, created, **kwargs):
        if notification and created:
            # what users to send to?
            # notification.send([to_user], 'discussion_post_save', {'from_user': from_user})
            pass

    def comment_notifications(sender, created, **kwargs):
        from django.contrib.auth.models import User
        user = User.objects.get(pk=1)
        if notification and created:
            notification.send([user], 'discussion_comment_save', {'': ''})
    notification.signals.post_save.connect(comment_notifications, sender=Comment)



