from celery import shared_task
import os
import sys
import logging
from .models import City, Country
from .HTTPclient import HTTPClient, HTTPError
from core.APICLients.externalAPI.city_country import CityExternalAPIClient
from django.db import transaction


def get_logger(level: str = logging.ERROR):
    _logger = logging.getLogger("solution_logger")
    _logger.setLevel(level)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    _logger.addHandler(handler)
    return _logger


logger = get_logger()

URL_CITY = os.getenv("URL_CITY")
CITY_TOKEN = os.getenv("CITY_TOKEN")

client_city = CityExternalAPIClient(HTTPClient(URL_CITY), CITY_TOKEN)


@transaction.atomic
def countries_generator(limit: int):
    offset = 0
    border = limit
    while countries := Country.objects.all()[offset:border]:
        yield countries
        offset += limit
        border += limit


@transaction.atomic
def cities_generator(limit: int):
    offset = 0
    border = limit
    while countries := City.objects.all()[offset:border]:
        yield countries
        offset += limit
        border += limit


@shared_task(name="country_update")
def country_update():
    for countries in countries_generator(10):
        for country_db in countries:
            try:
                country_from_api = client_city.get_country(country_db.id_country)
            except HTTPError:
                logger.error(f"HTTPError")
                continue
            Country.objects.filter(pk=country_db.pk).update(**country_from_api)


@shared_task(name="city_update")
def city_update():
    for cities in cities_generator(10):
        for city_db in cities:
            try:
                cities_from_api = client_city.get_city(city_db.name)
            except HTTPError:
                logger.error(f"HTTPError")
                continue
            for city in cities_from_api:
                if city["full_name"] == city_db.full_name:
                    del city["country"]
                    City.objects.filter(full_name=city_db.full_name).update(**city)
                    break






