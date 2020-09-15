import factory

from movies.factories import MovieFactory

from .models import Comment


class CommentFactory(factory.django.DjangoModelFactory):
    movie = factory.SubFactory(MovieFactory)
    body = factory.Faker('bs')

    class Meta:
        model = Comment
