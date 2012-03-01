from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import date, time


class Discussion(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    body = models.TextField()
    posts_file = models.FileField(upload_to='uploads/posts',
                                  blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Post by {user} at {time} on {date}'.format(
            user=self.user,
            time=time(self.time),
            date=date(self.time),
        )


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    body = models.TextField()
    comment_file = models.FileField(upload_to='uploads/comments',
                                    blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Comment by {user} at {time} on {date}'.format(
            user=self.user,
            time=time(self.time),
            date=date(self.time),
        )
