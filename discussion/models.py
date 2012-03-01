from django.contrib.auth.models import User
from django.db import models


class Discussion(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class Post(models.Model):
    discussion = models.ForeignKey(Discussion)
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    body = models.TextField()
    posts_file = models.FileField(upload_to='uploads/posts',
                                  blank=True, null=True)

    def __unicode__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)
    body = models.TextField()
    comment_file = models.FileField(upload_to='uploads/comments',
                                    blank=True, null=True)

    def __unicode__(self):
        return 'Comment on %s by %s' % (self.post.name, self.user)
