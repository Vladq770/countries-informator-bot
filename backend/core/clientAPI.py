import os
from abc import ABC, abstractmethod
import backoff
import environ
from aiohttp import ClientSession, ContentTypeError
from pydantic import BaseSettings
from functools import lru_cache
from .models import Cities, Countries, Weather
from .modelsAPI import Country, City

env = environ.Env()

@lru_cache(maxsize=None)
def get_aiohttp_client_session() -> ClientSession:
    return ClientSession()

class HTTPSettings(BaseSettings):
    HTTP_MAX_TRIES: int = 5
    HTTP_MAX_TIME: int = 10

    HTTP_TIMEOUT: int = 10
    HTTP_LIMIT_MAX_CONN: int = 12

    class Config(BaseSettings.Config):
        env_file = env.read_env()

class HTTPClient(ABC):
    settings = HTTPSettings()

    retry_policy = backoff.on_exception(
        backoff.expo,
        exception=BaseException,
        max_tries=settings.HTTP_MAX_TRIES,
        max_time=settings.HTTP_MAX_TIME
    )

    @abstractmethod
    @retry_policy
    async def get_city(self, name):
        pass

    @abstractmethod
    @retry_policy
    async def get_country(self, name):
        pass

    @abstractmethod
    @retry_policy
    async def get_weather(self, latitude, longitude):
        pass

    @abstractmethod
    @retry_policy
    async def get_currency(self):
        pass

class HTTPClientAPI(HTTPClient):
    def __init__(self, url_city, url_weather, url_currency, token_city, token_weather, token_currency):
        self._url_city = url_city
        self._url_weather = url_weather
        self._url_currency = url_currency
        self._token_city = token_city
        self._token_weather = token_weather
        self._token_currency = token_currency
