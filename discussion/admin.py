from django.contrib import admin
from discussion.models import Comment, Discussion, Post


class CommentInline(admin.TabularInline):
    extra = 1
    model = Comment
    raw_id_fields = ('user',)


class PostAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)
    list_filter = ('discussion',)


class DiscussionAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
