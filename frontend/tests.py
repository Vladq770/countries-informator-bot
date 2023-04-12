import os
import redis
import asyncio
from dotenv import load_dotenv
from HTTPClient import HTTPClient
from externalAPI import ExternalAPIClient

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
URL_BACKEND = os.getenv("URL_BACKEND")
http_client = ExternalAPIClient(HTTPClient(URL_BACKEND))
redis_instance = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))
latitude = "45.213"
longitude = "54.1373"


def test_city():
    asyncio.get_event_loop().run_until_complete(get_city())


def test_country():
    asyncio.get_event_loop().run_until_complete(get_country())


def test_weather():
    asyncio.get_event_loop().run_until_complete(get_weather())


def test_currency():
    asyncio.get_event_loop().run_until_complete(get_currency())


async def get_city():
    data = await http_client.get_city("тольятти")
    assert data["0"]["name"] == "Тольятти"
    assert data["0"]["country"] == "RU"
    assert data["0"]["full_name"] == "Тольятти (Самарская область)"


async def get_country():
    data = await http_client.get_country("ru")
    assert data["name"] == "Россия"
    assert data["fullname"] == "Российская Федерация"
    assert data["english"] == "Russia"


async def get_weather():
    data = await http_client.get_weather(latitude, longitude)
    """"С погодой не получится применить assert"""


async def get_currency():
    data = await http_client.get_currency("CN")
    assert data["Name"] == "Китайских юаней"


