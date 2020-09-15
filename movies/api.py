from django.conf import settings

import requests

from .exceptions import MovieDoesNotExist


class OMDbAPI:
    @classmethod
    def get_movie_by_title(cls, title):
        url = f'{settings.MOVIES_EXTERNAL_API}?apikey={settings.MOVIES_API_KEY}&t={title}'  # noqa: E501 WPS305
        try:
            response = requests.get(url, timeout=5)
        except requests.exceptions.RequestException:
            response_json = {}
        else:
            response_json = response.json()
        finally:
            if 'Error' in response_json:
                raise MovieDoesNotExist(response_json.get('Error'))
            return response_json
