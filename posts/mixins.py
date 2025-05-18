from django.shortcuts import get_object_or_404
from .models import Post


class MultipleFieldLookupMixin:
    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}

        post_id = Post.objects.get(slug=self.kwargs["slug"]).id
        filter['post'] = post_id
        filter['id'] = self.kwargs["id"]
        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj
