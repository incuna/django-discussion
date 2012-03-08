from django import forms

from discussion.models import Comment, Post, Discussion


class CommentForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'post')
        model = Comment


class PostForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'discussion')
        model = Post


class SearchForm(forms.Form):
    search = forms.CharField()
    discussion = forms.ModelChoiceField(required=False, queryset=Discussion.objects, empty_label='All discussions')
    #class Meta:
    #    exclude = ('discussion', 'slug')
    #    model = Post

