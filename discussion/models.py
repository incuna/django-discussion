import os

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import date, time
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from notification.models import NoticeType, create_notice_type, send
from orderable.models import Orderable


class Discussion(Orderable):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    image = models.ImageField(upload_to='images/discussions', max_length=255, blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('discussion', [self.slug])

    @property
    def notification_label(self):
        return "discussion_remind_%s" % self.slug

    @property
    def notification_display(self):
        return ("Notification for %s." % self.name)[:50]

    @property
    def notice_type(self):
        """
            Return the notice type for this discussion.
            If it does not exist then the notice type will be created.
        """
        self.create_notice_type()
        return NoticeType.objects.get(label=self.notification_label)

    def create_notice_type(self):
        """Create (or update) a notice type for discussion instance ."""
        create_notice_type(
                label=self.notification_label,
                display=self.notification_display,
                description="A new post has been added .",
                slug=self._meta.app_label,
                default=0)


class Post(models.Model):
    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    body = models.TextField()
    attachment = models.FileField(upload_to='uploads/posts', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-time',)

    def __unicode__(self):
        return 'Post by {user} at {time} on {date}'.format(
            user=self.user,
            time=time(self.time),
            date=date(self.time),
        )

    @models.permalink
    def get_absolute_url(self):
        return ('discussion_post', [self.discussion.slug, str(self.id)])

    @property
    def attachment_filename(self):
        return self.attachment and os.path.basename(self.attachment.name)

    @property
    def prefix(self):
        return 'post-%d' % (self.pk or 0,)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    body = models.TextField()
    attachment = models.FileField(upload_to='uploads/comments',
                                    blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    @property
    def attachment_filename(self):
        return self.attachment and os.path.basename(self.attachment.name)

    class Meta:
        ordering = ('time',)

    def __unicode__(self):
        return 'Comment by {user} at {time} on {date}'.format(
            user=self.user,
            time=time(self.time),
            date=date(self.time),
        )


@receiver(post_save, sender=Discussion)
def create_discussion_notice_type(sender, instance, **kwargs):
    # If display or diary title has changed notification details will be updated or created for new diary.
    instance.create_notice_type()


@receiver(pre_delete, sender=Discussion)
def delete_discussion_notice_type(sender, instance, **kwargs):
    instance.notice_type.delete()


def notify_discussion_subscribers(discussion, instance):
    """
        Notifies all users who have their notification settings set to True for given discussion
        instance parameter here is either Post or Comment
    """
    notification_label = discussion.notification_label
    users = User.objects.filter(
            noticesetting__send=True,
            noticesetting__notice_type__label=notification_label).exclude(id=instance.user.id).distinct()
    send(users, notification_label, {'discussion': discussion}, now=True)


def post_notifications(sender, instance, created, **kwargs):
    if created:
        notify_discussion_subscribers(instance.discussion, instance)
models.signals.post_save.connect(post_notifications, sender=Post)


def comment_notifications(sender, instance, created, **kwargs):
    if created:
        notify_discussion_subscribers(instance.post.discussion, instance)
models.signals.post_save.connect(comment_notifications, sender=Comment)

