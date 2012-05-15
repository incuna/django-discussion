from django.contrib import admin
from discussion.models import Comment, Discussion, Post
from orderable.admin import OrderableAdmin


class CommentInline(admin.TabularInline):
    extra = 1
    model = Comment
    raw_id_fields = ('user',)


class PostAdmin(admin.ModelAdmin):
    inlines = (CommentInline,)
    list_filter = ('discussion',)


class DiscussionAdmin(OrderableAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
