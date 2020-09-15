from django.db import models
from django.utils.translation import gettext_lazy as _

from .conf import MovieConf  # noqa: F401

NOT_AVAILABLE = 'N/A'


class Rating(models.Model):
    source = models.CharField(_('source'), max_length=50)
    value = models.CharField(_('value'), max_length=50)


class Movie(models.Model):
    title = models.CharField(_('title'), max_length=255)
    year = models.IntegerField(_('year'), blank=True, null=True)
    rated = models.CharField(_('rated'), max_length=50, default=NOT_AVAILABLE)
    released = models.DateField(_('released'), null=True)
    runtime = models.CharField(
        _('runtime'), max_length=50, default=NOT_AVAILABLE,
    )
    genre = models.CharField(_('genre'), max_length=50, default=NOT_AVAILABLE)
    director = models.CharField(
        _('director'), max_length=50, default=NOT_AVAILABLE,
    )
    writer = models.CharField(
        _('writer'), max_length=255, default=NOT_AVAILABLE,
    )
    actors = models.CharField(
        _('actors'), max_length=255, default=NOT_AVAILABLE,
    )
    plot = models.CharField(
        _('plot'), max_length=255, default=NOT_AVAILABLE,
    )
    language = models.CharField(
        _('language'), max_length=50, default=NOT_AVAILABLE,
    )
    country = models.CharField(
        _('country'), max_length=50, default=NOT_AVAILABLE,
    )
    awards = models.CharField(
        _('awards'), max_length=50, default=NOT_AVAILABLE,
    )
    poster = models.CharField(
        _('poster'), max_length=255, default=NOT_AVAILABLE,
    )
    ratings = models.ManyToManyField(Rating, default=[])
    metascore = models.CharField(
        _('metascore'), max_length=50, default=NOT_AVAILABLE,
    )
    imdb_rating = models.CharField(
        _('imdb_rating'), max_length=50, default=NOT_AVAILABLE,
    )
    imdb_votes = models.CharField(
        _('imdb_votes'), max_length=50, default=NOT_AVAILABLE,
    )
    imdb_id = models.CharField(
        _('imdb_id'), max_length=50, default=NOT_AVAILABLE,
    )
    type = models.CharField(
        _('type'), max_length=50, default=NOT_AVAILABLE,
    )
    dvd = models.DateField(_('dvd'), null=True)
    boxoffice = models.CharField(
        _('boxoffice'), max_length=50, default=NOT_AVAILABLE,
    )
    production = models.CharField(
        _('production'), max_length=50, default=NOT_AVAILABLE,
    )
    website = models.CharField(
        _('website'), max_length=50, default=NOT_AVAILABLE,
    )

    def __str__(self):
        return self.title
