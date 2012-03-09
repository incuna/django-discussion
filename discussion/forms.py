from django import forms

from discussion.models import Comment, Post, Discussion


class CommentForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'post')
        model = Comment
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder' : 'Reply to this conversation'}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'discussion')
        model = Post
        widgets = {
            'body' : forms.Textarea(attrs={'placeholder' : 'Start a conversation'}),
        }

class SearchForm(forms.Form):
    search = forms.CharField()
    discussion = forms.ModelChoiceField(required=False, queryset=Discussion.objects, empty_label='All discussions')
    #class Meta:
    #    exclude = ('discussion', 'slug')
    #    model = Post
    