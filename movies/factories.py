import factory

from .models import Movie


class MovieFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('bs')

    class Meta:
        model = Movie
