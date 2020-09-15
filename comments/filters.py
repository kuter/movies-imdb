import django_filters

from .models import Comment


class CommentFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Comment
        fields = ['movie', 'created_at']
