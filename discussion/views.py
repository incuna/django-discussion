from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DetailView, ListView, FormView
from django.views.generic.list import BaseListView
from django.db.models import Q

from discussion.forms import CommentForm, PostForm, SearchForm
from discussion.models import Discussion, Comment, Post
from discussion.utils import class_view_decorator


class SearchFormMixin(object):
    """Add the basic search form to your view."""

    search_initial = {}

    def get_context_data(self, **kwargs):
        context = super(SearchFormMixin, self).get_context_data(**kwargs)
        context['search_form'] = self.get_search_form(SearchForm)
        return context

    def get_search_form(self, form_class):
        """
        Returns an instance of the search form to be used in this view.
        """
        return form_class(**self.get_search_form_kwargs())

    def get_search_form_kwargs(self):
        """
        Returns the keyword arguments for instanciating the search form.
        """
        kwargs = {'initial': self.get_search_initial()}
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })

        return kwargs

    def get_search_initial(self):
        """
        Returns the initial data to use for search forms on this view.
        """
        return self.search_initial


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
class DiscussionView(SearchFormMixin, DetailView):
    model = Discussion

    def get_context_data(self, **kwargs):
        self.search_initial.update({'discussion': self.object})
        context = super(DiscussionView, self).get_context_data(**kwargs)
        context['form'] = PostForm()
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

@class_view_decorator(login_required)
class PostView(DiscussionMixin, CreateView):
    form_class = CommentForm
    model = Comment
    template_name = 'discussion/post_detail.html'
    ajax_form_valid_template_name = 'discussion/_comment_detail.html'
    ajax_form_invalid_template_name = 'discussion/comment_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.post_obj = self.get_post(kwargs['pk'])
        return super(PostView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(PostView, self).get_form_kwargs()
        instance = self.model(user=self.request.user, post=self.post_obj)
        kwargs.update({
            'instance': instance,
            'prefix': self.post_obj.prefix,
        })
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

    def form_valid(self, form):
        if self.request.is_ajax():
            self.object = form.save()
            self.template_name = self.ajax_form_valid_template_name
            return self.render_to_response(self.get_context_data(comment=self.object))
        else:
            return super(PostView, self).form_valid(form)

    def form_invalid(self, form):
       if self.request.is_ajax():
           self.template_name = self.ajax_form_invalid_template_name
           return self.render_to_response(self.get_context_data(form=form), status=400)
       else:
           return super(PostView, self).form_invalid(form)


@class_view_decorator(login_required)
class Search(BaseListView, FormView):
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
        search_term = form.cleaned_data['search']
        object_list = self.model.objects.filter(Q(body__icontains=search_term) |
                                                Q(comment__body__icontains=search_term))
        if form.cleaned_data.get('discussion', None) is not None:
            object_list = object_list.filter(discussion=form.cleaned_data['discussion'])

        return self.render_to_response(self.get_context_data(form=form,
                                                             object_list=object_list.distinct(),
                                                             search_term=search_term))

    def get_context_data(self, **kwargs):
        if 'form' in kwargs:
            kwargs.update({'search_form': kwargs.pop('form')})

        return super(Search, self).get_context_data(**kwargs)

    def get_queryset(self):
        """
        Don't like this currently. I don't want to display all() on a GET but
        don't want to stop subclassers from using this method themselves.
        """
        return self.model.objects.none()

    def get_success_url(self):
        """Defined in case we ever get sent to it by accident"""
        return reverse('discussion_search')
