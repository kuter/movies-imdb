from django.test import TestCase
from django.urls import reverse_lazy

import factory
from rest_framework.test import APIClient

from ..factories import CommentFactory, MovieFactory
from ..models import Comment


class CommentViewSetTests(TestCase):
    url = reverse_lazy('comment-list')

    def setUp(self):
        self.client = APIClient()

    def test_should_add_comment_to_movie(self):
        movie = MovieFactory.create()
        COMMENT_BODY = "TEST"
        payload = {
            "movie": movie.pk,
            "body": COMMENT_BODY
        }

        response = self.client.post(self.url, payload)

        self.assertTrue(
            Comment.objects.filter(movie=movie.pk, body=COMMENT_BODY).exists()
        )

    def test_should_allow_filtering_comments_by_movie_id(self):
        movie, _ = MovieFactory.create_batch(2)
        CommentFactory.create_batch(3, movie=factory.Iterator([movie, _]))
        url = f"{self.url}?movie={movie.pk}"

        response = self.client.get(url)

        self.assertEqual(response.json()['count'], 2)


    def test_should_fetch_list_of_all_comments_present_in_database(self):
        CommentFactory.create_batch(2)

        response = self.client.get(self.url)

        self.assertEqual(response.json()['count'], 2)


class TopCommentViewSetTests(TestCase):
    url = reverse_lazy('top-list')

    def setUp(self):
        self.client = APIClient()

    def test_should_return_movies_with_same_number_of_comments_on_same_position_in_the_ranking(self):
        movie_1, movie_2, movie_3, movie_4 = MovieFactory.create_batch(4)
        CommentFactory.create_batch(3, movie=movie_1)
        CommentFactory.create_batch(4, movie=factory.Iterator([movie_2, movie_3]))
        CommentFactory.create(movie=movie_4)
        expected_results = [
            {'movie': 1, 'rank': 1, 'total_comments': 3},
            {'movie': 2, 'rank': 2, 'total_comments': 2},
            {'movie': 3, 'rank': 2, 'total_comments': 2},
            {'movie': 4, 'rank': 3, 'total_comments': 1},
        ]

        response = self.client.get(self.url)


        self.assertListEqual(response.json()['results'], expected_results)
