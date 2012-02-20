from django import forms

from discussion.models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'post')
        model = Comment


class PostForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'discussion')
        model = Post


class SearchForm(forms.ModelForm):
    class Meta:
        exclude = ('discussion', 'slug')
        model = Post

