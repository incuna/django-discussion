from django.core import signals
from django.conf import settings
from django.utils.translation import ugettext_noop as _


if 'notification' in settings.INSTALLED_APPS:
    from notification import models as notification
    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type('discussion_post_save', _('Post Added'),
                                        _('A new post has been added.'))
        notification.create_notice_type('discussion_comment_save', _('Comment Added'),
                                        _('A new comment has been added.'))

    signals.post_syncdb.connect(create_notice_types, sender=notification)

