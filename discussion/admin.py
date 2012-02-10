from django.contrib import admin
from discussion.models import Comment, Discussion, Post


class PostAdmin(admin.ModelAdmin):
    list_filter = ('discussion',)

admin.site.register(Discussion)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

