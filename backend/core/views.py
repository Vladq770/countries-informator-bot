import os
from dotenv import load_dotenv
import aiohttp
from django.http import HttpResponse, HttpResponseNotFound
#from django.core.cache import cache
from .models import Cities, Countries, Weather
import json
import redis

load_dotenv()

CITY_TOKEN = os.getenv("CITY_TOKEN")
WEATHER_TOKEN = os.getenv("WEATHER_TOKEN")
CURRENCY_TOKEN = os.getenv("CURRENCY_TOKEN")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

CURRENCIES = {
    'AU': 'AUD', 'AZ': 'AZN', 'GB': 'GBR', 'AM': 'AMD', 'BY': 'BYN', 'BG': 'BGN', 'BR': 'BRL', 'HU': 'HUF', 'CN': 'CNY',
    'DK': 'DKK', 'US': 'USD', 'IN': 'INR', 'KZ': 'KZT', 'CA': 'CAD', 'KG': 'KGS', 'MD': 'MDL', 'NO': 'NOK', 'PL': 'PLN',
    'RO': 'RON', 'SG': 'SGD', 'TJ': 'TJS', 'TR': 'TRY', 'UZ': 'UZS', 'UA': 'UAH', 'CZ': 'CZK', 'SE': 'SEK', 'CH': 'CHF',
    'ZA': 'ZAR', 'KR': 'KRW', 'JP': 'JPY', 'RU': 'USD'
}

redis_instance = redis.StrictRedis(host=REDIS_HOST, port=int(REDIS_PORT))


def index(request):
    return HttpResponse("Test")


async def get_city(name):
    list_city = []
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://htmlweb.ru/geo/api.php?city_name={name}&json&api_key'
                               f'={CITY_TOKEN}') as resp:
            try:
                cities = await resp.json()
            except:
                return None
            for i in range(len(cities) - 2):

                country = Countries.objects.filter(id_country=cities[str(i)]['country']).first()
                if not country:
                    country = await get_country(cities[str(i)]['country'])
                    country.save()
                try:
                    city = Cities(country=country, name=cities[str(i)]['name'], area=cities[str(i)]['area'],
                                  telcod=cities[str(i)]['telcod'], latitude=cities[str(i)]['latitude'],
                                  longitude=cities[str(i)]['longitude'], time_zone=cities[str(i)]['time_zone'],
                                  tz=cities[str(i)]['tz'], english=cities[str(i)]['english'],
                                  rajon=cities[str(i)]['rajon'], sub_rajon=cities[str(i)]['sub_rajon'],
                                  iso=cities[str(i)]['iso'], vid=cities[str(i)]['vid'],
                                  post=cities[str(i)]['post'], full_english=cities[str(i)]['full_english'],
                                  full_name=cities[str(i)]['full_name'])
                except:
                    city = Cities(country=country, name=cities[str(i)]['name'], full_name=cities[str(i)]['full_name'])
                if cities[str(i)]['wiki']:
                    city.wiki = cities[str(i)]['wiki']
                city_check = Cities.objects.filter(full_name=city.full_name)
                if not city_check:
                    city.save()
                list_city.append(city)
            return list_city


async def get_country(name):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://htmlweb.ru/geo/api.php?country={name}&info&json&api_key'
                               f'={CITY_TOKEN}') as resp:
            c = await resp.json()
            if len(c) > 5:
                try:
                    country = Countries(name=c['country']['name'],
                                        english=c['country']['english'], fullname=c['country']['fullname'],
                                        id_country=c['country']['id'], country_code3=c['country']['country_code3'],
                                        iso=c['country']['iso'], telcod=c['country']['telcod'],
                                        location=c['country']['location'],
                                        mcc=c['country']['mcc'], capital=c['capital']['name'],
                                        lang=c['country']['lang'], langcod=c['country']['langcod'],
                                        time_zone=c['time_zone'], tz=c['tz'])
                except:
                    country = Countries(name=c['country']['name'],
                                        id_country=c['country']['id'])
                country_check = Countries.objects.filter(name=country.name)
                if not country_check:
                    country.save()
                return country
            return None


async def get_city_country(request, name, *args, **kwargs):
    country = Countries.objects.filter(name=name)
    if country:
        return HttpResponse(country)
    cities = Cities.objects.filter(name=name)
    if cities:
        return HttpResponse(list(cities))
    country = await get_country(name)
    if country:
        return HttpResponse(country)
    cities = await get_city(name)
    if cities:
        return HttpResponse(cities)
    return HttpResponseNotFound()


async def get_weather(request, latitude, longitude, *args, **kwargs):
    url_yandex = f'https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&extra=true'
    if f'{latitude}{longitude}' in redis_instance:
        return HttpResponse(redis_instance.get(f'{latitude}{longitude}'))
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url_yandex, headers={'X-Yandex-API-Key': WEATHER_TOKEN}) as resp:
            try:
                data = await resp.read()
            except:
                return HttpResponseNotFound()
            w = json.loads(data)
            weather = Weather(latitude=latitude, longitude=longitude, temp=w['fact']['temp'],
                              feels_like=w['fact']['feels_like'], condition=w['fact']['condition'],
                              wind_speed=w['fact']['wind_speed'], wind_gust=w['fact']['wind_gust'],
                              wind_dir=w['fact']['wind_dir'], pressure_mm=w['fact']['pressure_mm'],
                              humidity=w['fact']['humidity'])
            redis_instance.set(f'{latitude}{longitude}', str(weather), 1000)
    return HttpResponse(weather)


async def get_currency(request, code, *args, **kwargs):
    if code not in CURRENCIES:
        return HttpResponseNotFound()
    if code in redis_instance:
        return HttpResponse(redis_instance.get(code))
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.cbr-xml-daily.ru/daily_json.js') as resp:
            try:
                data = await resp.read()
            except:
                return HttpResponseNotFound()
            currencies = json.loads(data)
            currency = f'{currencies["Valute"][CURRENCIES[code]]["Nominal"]} {CURRENCIES[code]} = {currencies["Valute"][CURRENCIES[code]]["Value"]} RUB'
            redis_instance.set(code, currency, 15)
            return HttpResponse(currency)
