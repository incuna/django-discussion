from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView, FormView
from django.views.generic.list import BaseListView

from discussion.forms import CommentForm, PostForm, SearchForm
from discussion.models import Discussion, Comment, Post
from discussion.utils import class_view_decorator


class SearchFormMixin(object):
    """Add the basic search form to your view."""
    def get_context_data(self, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)
        context['search_form'] = SearchForm()
        return context


class DiscussionMixin(object):
    discussion_slug = 'discussion_slug'

    def dispatch(self, request, *args, **kwargs):
        self.discussion = self.get_discussion(slug=kwargs[self.discussion_slug])
        return super(DiscussionMixin, self).dispatch(request, *args, **kwargs)

    def get_discussion(self, slug=None):
        if slug is None:
            slug = self.kwargs[self.discussion_slug]
        return Discussion.objects.get(slug=slug)

    def get_queryset(self):
        qs = super(DiscussionMixin, self).get_queryset()
        return qs.filter(discussion=self.discussion)


@class_view_decorator(login_required)
class DiscussionList(SearchFormMixin, ListView):
    model = Discussion


@class_view_decorator(login_required)
class DiscussionView(DetailView):
    model = Discussion

    def get_context_data(self, **kwargs):
        context = super(DiscussionView, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['post_form'] = PostForm()
        return context


@class_view_decorator(login_required)
class CreatePost(DiscussionMixin, CreateView):
    form_class = PostForm
    model = Post

    def get_form_kwargs(self):
        kwargs = super(CreatePost, self).get_form_kwargs()
        instance = self.model(user=self.request.user, discussion=self.discussion)
        kwargs.update({'instance': instance})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['discussion'] = self.discussion
        return context

    def get_success_url(self):
        kwargs = {'slug': self.kwargs[self.discussion_slug]}
        return reverse('discussion', kwargs=kwargs)


@class_view_decorator(login_required)
class PostView(DiscussionMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'discussion/post_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = self.get_post(kwargs['pk'])
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostView, self).get_form_kwargs()
        instance = self.model(user=self.request.user, post=self.post_obj)
        kwargs.update({'instance': instance})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['post'] = self.post_obj
        return context

    def get_post(self, pk=None):
        if pk is None:
            pk = self.kwargs['pk']
        return Post.objects.get(pk=pk)

    def get_success_url(self):
        kwargs = {
            'pk': self.kwargs['pk'],
            'discussion_slug': self.kwargs[self.discussion_slug]
        }
        return reverse('discussion_post', kwargs=kwargs)


@class_view_decorator(login_required)
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
        return reverse('discussion_search')
