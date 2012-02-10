from django.conf.urls.defaults import *

from discussion.views import DiscussionList, DiscussionView, PostList, PostView


urlpatterns = patterns('discussion.views',
    url(r'^$', DiscussionList.as_view()),
    url(r'^(?P<slug>[\w-]+)/$', DiscussionView.as_view(), name='discussion'),
    url(r'^(?P<discussion_slug>[\w-]+)/posts/$', PostList.as_view()),
    url(r'^(?P<discussion_slug>[\w-]+)/posts/(?P<slug>[\w-]+)/$', PostView.as_view(), name='post'),

    # url(r'^(?P<discussion_slug>[\w-]+)/posts/', include(patterns(
    #     url(r'^$', PostList.as_view()),
    #     url(r'^(?P<slug>[\w-]+)/$', PostView.as_view()),
    # ))
)

