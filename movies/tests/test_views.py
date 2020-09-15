# flake8: noqa: E501
import json
from pathlib import Path
import datetime

from django.utils.text import slugify
from django.conf import settings
from django.test import TestCase
from django.urls import reverse_lazy

from requests.exceptions import ReadTimeout
import responses
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from ..models import Movie

JSON_RESPONSES_DIR = Path(__file__).parent / 'responses'


class MovieViewSetTests(TestCase):
    url = reverse_lazy('movie-list')

    def setUp(self):
        self.client = APIClient()

    def _add_response_for_title(self, title):
        with open(JSON_RESPONSES_DIR / f'{slugify(title)}.json') as f:
            data = json.load(f)
        responses.add(
            responses.GET,
            settings.MOVIES_EXTERNAL_API,
            json=data,
            status=HTTP_200_OK
        )


    def test_should_return_200_on_get(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, HTTP_200_OK)

    @responses.activate
    def test_should_fetch_and_save_movie(self):
        self._add_response_for_title('Terminator')

        response = self.client.post(self.url, data={'title': 'Terminator'})

        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertTrue(Movie.objects.filter(title='Terminator').exists())

    @responses.activate
    def test_should_raise_exception(self):
        responses.add(
            responses.GET,
            settings.MOVIES_EXTERNAL_API,
            json={'Response': 'False', 'Error': 'API TEST ERROR'},
            status=HTTP_200_OK,
        )

        response = self.client.post(self.url, data={'title': 'Not found'})

        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['detail'], 'API TEST ERROR')

    @responses.activate
    def test_should_raise_exception_on_timeout(self):
        responses.add(
            responses.GET,
            settings.MOVIES_EXTERNAL_API,
            body=ReadTimeout(),
            status=HTTP_200_OK,
        )

        response = self.client.post(self.url, data={'title': 'Misery'})

        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_should_store_released_as_date(self):
        self._add_response_for_title('Home Alone')

        self.client.post(self.url, data={'title': 'Home Alone'})
        movie = Movie.objects.get(title='Home Alone')

        self.assertTrue(isinstance(movie.released, datetime.date))

    @responses.activate
    def test_should_store_dvd_as_date(self):
        self._add_response_for_title('Pulp Fiction')

        self.client.post(self.url, data={'title': 'Pulp Fiction'})
        movie = Movie.objects.get(title='Pulp Fiction')

        self.assertTrue(isinstance(movie.dvd, datetime.date))

    @responses.activate
    def test_should_return_response_with_full_movie_object(self):
        self._add_response_for_title('et')
        expected_json = {
            'actors': 'Dee Wallace, Henry Thomas, Peter Coyote, Robert MacNaughton',
            'awards': 'Won 4 Oscars. Another 48 wins & 35 nominations.',
            'boxoffice': 'N/A',
            'country': 'USA',
            'director': 'Steven Spielberg',
            'dvd': '2002-10-22',
            'genre': 'Family, Sci-Fi',
            'imdb_id': 'tt0083866',
            'imdb_rating': '7.8',
            'imdb_votes': '361,031',
            'language': 'English',
            'metascore': '91',
            'plot': 'A troubled child summons the courage to help a friendly alien escape '
            'Earth and return to his home world.',
            'poster': 'https://m.media-amazon.com/images/M/MV5BMTQ2ODFlMDAtNzdhOC00ZDYzLWE3YTMtNDU4ZGFmZmJmYTczXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SX300.jpg',
            'production': 'Universal Pictures',
            'rated': 'PG',
            'ratings': [
                {'source': 'Internet Movie Database', 'value': '7.8/10'},
                {'source': 'Rotten Tomatoes', 'value': '98%'},
                {'source': 'Metacritic', 'value': '91/100'}
            ],
            'released': '1982-06-11',
            'runtime': '115 min',
            'title': 'E.T. the Extra-Terrestrial',
            'type': 'movie',
            'website': 'N/A',
            'writer': 'Melissa Mathison',
            'year': 1982}

        response = self.client.post(self.url, data={'title': 'ET'})

        self.assertDictEqual(response.json(), expected_json)
