# flake8: noqa: N815
from datetime import datetime
from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Movie, Rating



class CustomDateField(serializers.DateField):
    def to_internal_value(self, data):
        try:
            ret = datetime.strptime(data, '%d %b %Y').date()
        except ValueError:
            ret = None
        return ret


class RatingAPISerializer(serializers.ModelSerializer):
    Source = serializers.CharField(source='source')
    Value = serializers.CharField(source='value')

    class Meta:
        model = Rating
        fields = ('Source', 'Value')

class MovieAPISerializer(WritableNestedModelSerializer):
    Title = serializers.CharField(source='title')
    Year = serializers.IntegerField(source='year')
    Rated = serializers.CharField(source='rated')
    Released = CustomDateField(source='released')
    Runtime = serializers.CharField(source='runtime')
    Genre = serializers.CharField(source='genre')
    Director = serializers.CharField(source='director')
    Writer = serializers.CharField(source='writer')
    Actors = serializers.CharField(source='actors')
    Plot = serializers.CharField(source='plot')
    Language = serializers.CharField(source='language')
    Country = serializers.CharField(source='country')
    Awards = serializers.CharField(source='awards')
    Poster = serializers.CharField(source='poster')
    Ratings = RatingAPISerializer(many=True, source='ratings')
    Metascore = serializers.CharField(source='metascore')
    imdbRating = serializers.CharField(source='imdb_rating')
    imdbVotes = serializers.CharField(source='imdb_votes')
    imdbID = serializers.CharField(source='imdb_id')
    Type = serializers.CharField(source='type')
    DVD = CustomDateField(source='dvd')
    BoxOffice = serializers.CharField(source='boxoffice')
    Production = serializers.CharField(source='production')
    Website = serializers.CharField(source='website')

    class Meta:
        model = Movie
        fields = (
            'Title', 'Year', 'Rated', 'Released', 'Runtime', 'Genre',
            'Director', 'Writer', 'Actors', 'Plot', 'Language', 'Country',
            'Awards', 'Poster', 'Ratings', 'Metascore', 'imdbRating',
            'imdbVotes', 'imdbID', 'Type', 'DVD', 'BoxOffice', 'Production',
            'Website',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Movie.objects.all(), fields=['Title', 'imdbID']
            )
        ]


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class MovieSerializer(WritableNestedModelSerializer):
    ratings = RatingSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = '__all__'
