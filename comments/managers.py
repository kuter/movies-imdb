from django.db import models
from django.db.models import Count
from django.db.models.expressions import F, Window
from django.db.models.functions import DenseRank


class CommentManager(models.Manager):
    def top(self):
        return super().get_queryset().values(
            'movie',
        ).annotate(
            total_comments=Count('id'),
            rank=Window(
                expression=DenseRank(),
                order_by=F('total_comments').desc(),
            ),
        ).order_by('-total_comments')
