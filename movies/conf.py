from appconf import AppConf


class MovieConf(AppConf):
    EXTERNAL_API = 'http://www.omdbapi.com/'
    API_KEY = ''  # omdbapi API KEY
