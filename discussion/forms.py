from django import forms

from discussion.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'post')
        model = Comment

