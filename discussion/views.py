from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView

from discussion.forms import CommentForm
from discussion.models import Discussion, Comment, Post


class DiscussionList(ListView):
    model = Discussion


class DiscussionView(DetailView):
    model = Discussion


class PostList(ListView):
    model = Post


class PostView(CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'discussion/post_detail.html'

    def get_form_kwargs(self):
        kwargs = super(PostView, self).get_form_kwargs()
        instance = self.model(user=self.request.user, post=self.get_post())
        kwargs.update({'instance': instance})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = self.get_post()
        return context

    def get_post(self):
        return Post.objects.get(slug=self.kwargs['slug'])

    def get_success_url(self):
        kwargs = {
            'slug': self.kwargs['slug'],
            'discussion_slug': self.kwargs['discussion_slug']
        }
        return reverse('post', kwargs=kwargs)

