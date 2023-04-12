import os
from dotenv import load_dotenv
from HTTPClient import HTTPClient, HTTPError
from externalAPI import ExternalAPIClient
import aioredis
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from loader import dp, config, bot
from states import BotState
from text.inline import keyboards, choose_city_button
from text.keyboard import search_kb, chosen_country_kb, chosen_city_kb, search_city_kb, search_country_kb
from text.schemas import City, Country, Currency, Weather
import json

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
URL_BACKEND = os.getenv("URL_BACKEND")
REDIS_EXPIRATION_TIME = int(os.getenv("REDIS_EXPIRATION_TIME"))
http_client = ExternalAPIClient(HTTPClient(URL_BACKEND))
redis_instance = aioredis.from_url(f'redis://{REDIS_HOST}:{REDIS_PORT}')


@dp.callback_query_handler(state=BotState.choose_city_from_list)
async def process_callback(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data_cities = await state.get_data()
    i = callback_query.data[1:]
    data_city = data_cities["city"][i]
    await BotState.chosen_city.set()
    await state.update_data(city=data_city)
    await state.update_data(code=data_city["country"])
    await callback_query.message.edit_reply_markup()
    if callback_query.from_user.locale.language == "ru":
        await bot.send_message(callback_query.from_user.id, City(**data_city).to_message_ru(),
                               reply_markup=chosen_city_kb["ru"])
    else:
        await bot.send_message(callback_query.from_user.id, City(**data_city).to_message_en(),
                               reply_markup=chosen_city_kb["en"])


@dp.message_handler(Text(equals="Поиск города", ignore_case=True), state="*")
async def search_city(message: Message, state: FSMContext):
    await BotState.choose_name_city.set()
    await message.answer("Введите название", reply_markup=search_city_kb["ru"])


@dp.message_handler(Text(equals="Search city", ignore_case=True), state="*")
async def search_city(message: Message, state: FSMContext):
    await BotState.choose_name_city.set()
    await message.answer("Enter a name", reply_markup=search_city_kb["en"])


@dp.message_handler(Text(equals="Поиск страны", ignore_case=True), state="*")
async def search_country(message: Message, state: FSMContext):
    await BotState.choose_name_country.set()
    await message.answer("Введите название", reply_markup=search_country_kb["ru"])


@dp.message_handler(Text(equals="Search country", ignore_case=True), state="*")
async def search_country(message: Message, state: FSMContext):
    await BotState.choose_name_country.set()
    await message.answer("Enter a name", reply_markup=search_country_kb["en"])


@dp.message_handler(state=BotState.choose_name_country)
async def choose_name_country(message: Message, state: FSMContext):
    code = message.from_user.locale.language
    try:
        data = await http_client.get_country(message.text)
    except HTTPError:
        if code == "ru":
            await message.answer("Не найдено", reply_markup=search_kb["ru"])
            return
        else:
            await message.answer("Not found", reply_markup=search_kb["en"])
            return
    if code == "ru":
        await message.answer(Country(**data).to_message_ru(), reply_markup=chosen_country_kb["ru"])
    else:
        await message.answer(Country(**data).to_message_en(), reply_markup=chosen_country_kb["en"])
    await state.update_data(country=data)
    await state.update_data(code=data["id_country"])
    await BotState.chosen_country.set()


@dp.message_handler(state=BotState.choose_name_city)
async def choose_name_city(message: Message, state: FSMContext):
    code = message.from_user.locale.language
    try:
        data = await http_client.get_city(message.text)
    except HTTPError:
        if code == "ru":
            await message.answer("Не найдено", reply_markup=search_kb["ru"])
            return
        else:
            await message.answer("Not found", reply_markup=search_kb["en"])
            return
    if len(data) == 1:
        await state.update_data(code=data["0"]["country"])
        await state.update_data(city=data["0"])
        await BotState.chosen_city.set()
        if code == "ru":
            await message.answer(City(**data["0"]).to_message_ru(), reply_markup=chosen_city_kb["ru"])
        else:
            await message.answer(City(**data["0"]).to_message_en(), reply_markup=chosen_city_kb["en"])
        return
    await state.update_data(city=data)
    mes = ""
    if code == "ru":
        for i in range(len(data)):
            mes += f"{i+1}. {data[str(i)]['full_name']}\n"
        await message.answer(mes, reply_markup=choose_city_button(len(data)))
        await message.answer(f"Выберите город", reply_markup=search_kb["ru"])
    else:
        for i in range(len(data)):
            mes += f"{i+1}. {data[str(i)]['full_english']}\n"
        await message.answer(mes, reply_markup=choose_city_button(len(data)))
        await message.answer(f"Choose city", reply_markup=search_kb["en"])
    await BotState.choose_city_from_list.set()


@dp.message_handler(Text(equals="Валюта", ignore_case=True),
                    state=[BotState.chosen_country, BotState.chosen_city])
async def currency(message: Message, state: FSMContext):
    data_for_code = await state.get_data()
    code = data_for_code["code"]
    data = await redis_instance.get(f"{code}:bot")
    if data:
        data = json.loads(data)
        await message.answer(Currency(**data).to_message_ru(code))
        return
    try:
        data_currency = await http_client.get_currency(code)
    except HTTPError:
        await message.answer("Не найдено")
        return
    mes = Currency(**data_currency).to_message_ru(code)
    await redis_instance.set(f"{code}:bot", json.dumps(data_currency), REDIS_EXPIRATION_TIME)
    await message.answer(mes)


@dp.message_handler(Text(equals="Currency", ignore_case=True),
                    state=[BotState.chosen_country, BotState.chosen_city])
async def currency(message: Message, state: FSMContext):
    data_for_code = await state.get_data()
    code = data_for_code["code"]
    data = await redis_instance.get(f"{code}:bot")
    if data:
        data = json.loads(data)
        await message.answer(Currency(**data).to_message_ru(code))
        return
    try:
        data_currency = await http_client.get_currency(code)
    except HTTPError:
        await message.answer("Not Found")
        return
    mes = Currency(**data_currency).to_message_en(code)
    await redis_instance.set(f"{code}:bot", json.dumps(data_currency), REDIS_EXPIRATION_TIME)
    await message.answer(mes)


@dp.message_handler(Text(equals="Погода", ignore_case=True), state=BotState.chosen_city)
async def weather(message: Message, state: FSMContext):
    data_for_weather = await state.get_data()
    lat = data_for_weather["city"]["latitude"]
    lon = data_for_weather["city"]["longitude"]
    data = await redis_instance.get(f"{lat}:{lon}.bot")
    if data:
        data = json.loads(data)
        await message.answer(Weather(**data).to_message_ru())
        return
    try:
        data_weather = await http_client.get_weather(lat, lon)
    except HTTPError:
        await message.answer("Не найдено")
        return
    mes = Weather(**data_weather).to_message_ru()
    await redis_instance.set(f"{lat}:{lon}:bot", json.dumps(data_weather), REDIS_EXPIRATION_TIME)
    await message.answer(mes)


@dp.message_handler(Text(equals="Weather", ignore_case=True), state=BotState.chosen_city)
async def weather(message: Message, state: FSMContext):
    data_for_weather = await state.get_data()
    lat = data_for_weather["city"]["latitude"]
    lon = data_for_weather["city"]["longitude"]
    data = await redis_instance.get(f"{lat}:{lon}.bot")
    if data:
        data = json.loads(data)
        await message.answer(Weather(**data).to_message_ru())
        return
    try:
        data_weather = await http_client.get_weather(lat, lon)
    except HTTPError:
        await message.answer("Not Found")
        return
    mes = Weather(**data_weather).to_message_en()
    await redis_instance.set(f"{lat}:{lon}.bot", json.dumps(data_weather), REDIS_EXPIRATION_TIME)
    await message.answer(mes)


