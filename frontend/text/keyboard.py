from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_search_city_ru = KeyboardButton('Поиск города')
button_search_country_ru = KeyboardButton('Поиск страны')
button_weather_ru = KeyboardButton('Погода')
button_currency_ru = KeyboardButton('Валюта')
button_search_city_en = KeyboardButton('Search city')
button_search_country_en = KeyboardButton('Search country')
button_weather_en = KeyboardButton('Weather')
button_currency_en = KeyboardButton('Currency')

search_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(button_search_city_ru, button_search_country_ru)
search_city_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(button_search_country_ru)
search_country_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).add(button_search_city_ru)
chosen_city_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).row(button_search_city_ru, button_search_country_ru)
chosen_city_kb_ru.row(button_currency_ru, button_weather_ru)
chosen_country_kb_ru = ReplyKeyboardMarkup(resize_keyboard=True).row(button_search_city_ru, button_search_country_ru,
                                                                     button_currency_ru)
search_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add(button_search_city_en, button_search_country_en)
search_city_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add(button_search_country_en)
search_country_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).add(button_search_city_en)
chosen_city_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).row(button_search_city_en, button_search_country_en)
chosen_city_kb_en.row(button_currency_en, button_weather_en)
chosen_country_kb_en = ReplyKeyboardMarkup(resize_keyboard=True).row(button_search_city_en, button_search_country_en,
                                                                     button_currency_en)

search_kb = {"ru": search_kb_ru, "en": search_kb_en}
search_city_kb = {"ru": search_city_kb_ru, "en": search_city_kb_en}
search_country_kb = {"ru": search_country_kb_ru, "en": search_country_kb_en}
chosen_city_kb = {"ru": chosen_city_kb_ru, "en": chosen_city_kb_en}
chosen_country_kb = {"ru": chosen_country_kb_ru, "en": chosen_country_kb_en}
