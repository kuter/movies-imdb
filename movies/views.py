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
    create_serializer_class = CreateMovieSerializer
    api = OMDbAPI

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.create_serializer_class
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        api_serializer = self.get_serializer(data=request.data)
        api_serializer.is_valid(raise_exception=True)
        serializer = self.perform_create(api_serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def perform_create(self, serializer):
        obj = self.api.get_movie_by_title(**serializer.validated_data)
        serializer = self.serializer_class(data=obj)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer
