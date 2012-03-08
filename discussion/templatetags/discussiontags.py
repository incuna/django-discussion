import re
from django import template
from discussion.forms import CommentForm
from django.utils.safestring import mark_safe

re_img = re.compile(r'\.(bmp|jpe?g|jp2|jxr|gif|png|tiff?)$', re.IGNORECASE)

register = template.Library()

@register.inclusion_tag('discussion/limit_comments.html')
def limit_comments(post, first=2, last=1, limit=None, comments=None):
    """
    Render a limited set of comments for a post.
        first: The number of comments to display from the start of the list.
        last: The number of comments to display from the end of the list.
        limit: If there are less comments than this limit then display all comments.
            This defaults to first + last.
        comments: A list of comments to use (The default is the posts comments).

    {% limit_comments post 3 2 %}
    """
    
    if limit is None:
        limit = first+last
    if comments is None:
        comments = post.comment_set.all().select_related('post', 'post__discussion')

    count = comments.count()

    if count > limit:
        first_comments = comments[:first]
        last_comments = comments[count-last:]
        hidden_count = count-first-last
    else:
        first_comments = comments
        last_comments = None
        hidden_count = 0

    return {
        'post': post,
        'all_comments': comments,
        'first_comments': first_comments,
        'last_comments': last_comments,
        'all_count': count,
        'hidden_count': hidden_count,
    }


@register.inclusion_tag('discussion/comment_form.html')
def comment_form(post):
    """
    Render the comment form with the correct prefix.
    """
    return {
        'post': post,
        'form': CommentForm(prefix=post.prefix),
    }


@register.filter
def is_image(value):
    """
    Is the file an image (based on it's extension)
    """
    return re_img.search(value.name)


@register.filter
def highlight(text, word):
    return mark_safe(text.replace(word, "<span class='highlight'>%s</span>" % word))

