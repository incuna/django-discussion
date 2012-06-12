from django import forms
from django.utils.translation import ugettext_lazy as _

from discussion.models import Comment, Post, Discussion
from notification.models import NoticeSetting


class CommentForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'post')
        model = Comment
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': _('Reply to this conversation')}),
        }


class PostForm(forms.ModelForm):
    class Meta:
        exclude = ('user', 'discussion')
        model = Post
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': _('Start a conversation')}),
        }


class SearchForm(forms.Form):
    search = forms.CharField()
    discussion = forms.ModelChoiceField(
            required=False,
            queryset=Discussion.objects,
            empty_label=_('All discussions'))


class SubscribeForm(forms.Form):
    send = forms.ModelMultipleChoiceField(
            NoticeSetting.objects,
            required=False,
            label=_('Notify me with updates from this discussion by'),
            widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs')
        super(SubscribeForm, self).__init__(*args, **kwargs)
        self.fields['send'].queryset = qs
