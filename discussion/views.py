from django.views.generic import DetailView, ListView

from discussion.models import Discussion, Post


class DiscussionList(ListView):
    model = Discussion


class DiscussionView(DetailView):
    model = Discussion


class PostList(ListView):
    model = Post


class PostView(DetailView):
    model = Post

