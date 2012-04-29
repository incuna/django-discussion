from haystack import indexes
from .models import Discussion, Post


class DiscussionIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(model_attr='name')
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Discussion

    def index_queryset(self):
        return self.get_model().objects.all()


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    title = indexes.CharField(use_template=True)
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Post

    def index_queryset(self):
        return self.get_model().objects.all()


