import os 
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import date, time


class Discussion(models.Model):
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

class Post(models.Model):
    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    body = models.TextField()
    attachment = models.FileField(upload_to='uploads/posts', blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

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
