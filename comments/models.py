from django.db import models

from movies.models import Movie

from .managers import CommentManager


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    body = models.TextField()

    objects = CommentManager()

    def __str__(self):
        return self.movie.title
