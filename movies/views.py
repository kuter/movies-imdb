from rest_framework import status, viewsets
from rest_framework.response import Response

from .api import OMDbAPI
from .filters import MovieFilter
from .models import Movie
from .serializers import CreateMovieSerializer, MovieAPISerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieAPISerializer
    filterset_class = MovieFilter
    serializer_class = CreateMovieSerializer
    api = OMDbAPI

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        api_serializer = self.perform_create(serializer)
        headers = self.get_success_headers(api_serializer.data)
        return Response(
            api_serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        obj = self.api.get_movie_by_title(serializer.validated_data['title'])
        serializer = MovieAPISerializer(data=obj)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer
