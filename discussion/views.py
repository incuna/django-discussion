from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView, FormView
from django.views.generic.list import BaseListView

from discussion.forms import CommentForm, SearchForm
from discussion.models import Discussion, Comment, Post


class SearchFormMixin(object):
    """Add the basic search form to your view."""
    def get_context_data(self, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class DiscussionList(SearchFormMixin, ListView):
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


class Search(SearchFormMixin, BaseListView, FormView):
    form_class = SearchForm
    model = Post
    template_name = 'discussion/search.html'

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form,
                                        object_list=self.get_queryset()))

    def form_valid(self, form):
        """
        Using the name field try to find any posts that match.
        """
        object_list = self.model.objects.filter(name__icontains=form.cleaned_data['name'])
        return self.render_to_response(self.get_context_data(object_list=object_list))

    def get_queryset(self):
        """
        Don't like this currently. I don't want to display all() on a GET but
        don't want to stop subclassers from using this method themselves.
        """
        return self.model.objects.none()

    def get_success_url(self):
        """Defined in case we ever get sent to it by accident"""
        return reverse('search')

