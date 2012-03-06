from django import template

register = template.Library()

@register.inclusion_tag('discussion/limit_comments.html')
def limit_comments(post, first=2, last=1, limit=None, comments=None):
    """
    Simple tag to limit the comments being displayed.
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

