import os
from dotenv import load_dotenv
from rest_framework.response import Response
from .HTTPclient import HTTPClient, HTTPError
from core.APICLients.externalAPI import city_country, weather, currency
from core.APICLients.externalAPIForTests import cityTest, weatherTest, currencyTest
from .models import City, Country
import redis
from rest_framework import status
from rest_framework.decorators import api_view
import json
from .serializers import CitySerializer, CountrySerializer


load_dotenv()


URL_WEATHER = os.getenv("URL_WEATHER")
URL_CITY = os.getenv("URL_CITY")
URL_CURRENCY = os.getenv("URL_CURRENCY")
CITY_TOKEN = os.getenv("CITY_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
CURRENCY_TOKEN = os.getenv("CURRENCY_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_EXPIRATION_TIME = int(os.getenv("REDIS_EXPIRATION_TIME"))
TEST = os.getenv("TEST")

if TEST == "True":
    weather = weatherTest
    city_country = cityTest
    currency = currencyTest

client_weather = weather.WeatherExternalAPIClient(
    HTTPClient(URL_WEATHER, extra_request_params={"headers":
                                                      {"X-Yandex-API-Key": WEATHER_TOKEN}})
)
client_currency = currency.CurrencyExternalAPIClient(HTTPClient(URL_CURRENCY))
client_city = city_country.CityExternalAPIClient(HTTPClient(URL_CITY), CITY_TOKEN)
redis_instance = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))


@api_view(['GET'])
def index(request):
    d = {'test': 1, 'TEST': 'qwerty'}
    return Response(d)


def get_city_from_api(name):
    cities = {}
    index_city = 0
    try:
        data = client_city.get_city(name)
    except HTTPError:
        return None
    for city_from_api in data:
        country = Country.objects.filter(id_country=city_from_api['country']).first()
        if not country:
            country = Country(**get_country_from_api(city_from_api['country'], save=False))
            country.save()
        code = city_from_api.pop('country')
        city = City(country=country, **city_from_api)
        city_check = City.objects.filter(full_name=city.full_name)
        if not city_check:
            city.save()
        city_from_api['country'] = code
        cities[str(index_city)] = city_from_api
        index_city += 1
    return cities


def get_country_from_api(name, save=True):
    try:
        data = client_city.get_country(name)
    except HTTPError:
        return None
    country = Country(**data)
    country_check = Country.objects.filter(name=country.name)
    if not country_check and save:
        country.save()
    return data


@api_view(['GET'])
def get_city(request, name, *args, **kwargs):
    if cities := City.objects.filter(name=name):
        cities_response = {}
        index_city = 0
        for city in cities:
            serializer = CitySerializer(city)
            cities_response[str(index_city)] = serializer.data
            cities_response[str(index_city)]["country"] = city.country.id_country
            index_city += 1
        return Response(cities_response)
    if cities := get_city_from_api(name):
        return Response(cities)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_country(request, name, *args, **kwargs):
    if country := Country.objects.filter(name=name).first():
        serializer = CountrySerializer(country)
        return Response(serializer.data)
    if country := get_country_from_api(name):
        return Response(country)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_weather(request, latitude, longitude, *args, **kwargs):
    if f'{latitude}:{longitude}' in redis_instance:
        return Response(json.loads(redis_instance.get(f'{latitude}:{longitude}')))
    try:
        weather = client_weather.get_weather(latitude, longitude)
    except HTTPError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    redis_instance.set(f'{latitude}:{longitude}', json.dumps(weather), REDIS_EXPIRATION_TIME)
    return Response(weather)


@api_view(['GET'])
def get_currency(request, code, *args, **kwargs):
    if code in redis_instance:
        return Response(json.loads(redis_instance.get(code)))
    try:
        currency = client_currency.get_currency(code)
    except HTTPError:
        return Response(status=status.HTTP_404_NOT_FOUND)
    redis_instance.set(code, json.dumps(currency), REDIS_EXPIRATION_TIME)
    return Response(currency)

