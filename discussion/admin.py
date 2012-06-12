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
    list_display = ('discussion', 'time')


class DiscussionAdmin(OrderableAdmin):
    prepopulated_fields = {
        'slug': ('name',)
    }
    list_display = ('name', 'description')


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
