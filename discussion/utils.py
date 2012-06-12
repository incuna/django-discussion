from django.utils.decorators import method_decorator
from django.conf import settings


def class_view_decorator(function_decorator):
    """Convert a function based decorator into a class based decorator usable
    on class based Views.

    Follows the general idea from https://docs.djangoproject.com/en/dev/topics/class-based-views/#decorating-the-class.

    Can't subclass the `View` as it breaks inheritance (super in particular),
    so we monkey-patch instead.
    """

    def simple_decorator(View):
        View.dispatch = method_decorator(function_decorator)(View.dispatch)
        return View

    return simple_decorator


# If this is set to `[]`, no uploads will be accepted.
# If it is set to `None`, the whitelist will not be used.
DISCUSSION_UPLOAD_EXTENSIONS = getattr(settings, 'DISCUSSION_UPLOAD_EXTENSIONS', [
    'odt', 'odf', 'odp',  # Open/LibreOffice
    'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx',  # MS Office
    'pdf', 'gif', 'jpg', 'jpeg', 'png',  # Other sane defaults...
])


def file_extension(path):
    """Get the file extension of a path/filename."""
    return path.split('/')[-1].split('.')[-1]
