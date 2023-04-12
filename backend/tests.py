import pytest
from urllib.parse import urljoin
import json
import redis
import requests
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
URL_BACKEND = os.getenv("URL_BACKEND")
redis_instance = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))
temp: float
value: float


@pytest.fixture
def get_coordinates():
    return 13.1245, 45.346


def test_city_api():
    response = requests.get(urljoin(URL_BACKEND, "city/тольятти"))
    data = response.json()
    assert response.status_code == 200
    assert data["0"]["name"] == "Тольятти"
    assert data["0"]["country"] == "RU"
    assert data["0"]["full_name"] == "Тольятти (Самарская область)"


def test_country_api():
    response = requests.get(urljoin(URL_BACKEND, "country/ru"))
    data = response.json()
    assert response.status_code == 200
    assert data["name"] == "Россия"
    assert data["fullname"] == "Российская Федерация"
    assert data["english"] == "Russia"


def test_weather_api(get_coordinates):
    latitude, longitude = get_coordinates
    response = requests.get(urljoin(URL_BACKEND, f"weather/{latitude}/{longitude}"))
    data = response.json()
    global temp
    temp = data["temp"]
    assert response.status_code == 200


def test_weather_redis(get_coordinates):
    latitude, longitude = get_coordinates
    temp_redis = json.loads(redis_instance.get(f"{latitude}:{longitude}"))["temp"]
    assert temp == temp_redis


def test_currency_api():
    response = requests.get(urljoin(URL_BACKEND, "currency/US"))
    data = response.json()
    global value
    value = data["Value"]
    assert response.status_code == 200


def test_currency_redis():
    value_redis = json.loads(redis_instance.get(f"US"))["Value"]
    assert value == value_redis
