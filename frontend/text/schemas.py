from pydantic import BaseModel


class City(BaseModel):
    country: str = ""
    name: str = ""
    area: int = 0
    telcod: str = ""
    latitude: str = ""
    longitude: str = ""
    time_zone: int = 0
    tz: str = ""
    english: str = ""
    rajon: int = 0
    sub_rajon: int = 0
    iso: str = ""
    vid: int = 0
    post: str = ""
    wiki: str = ""
    full_english: str = ""
    full_name: str = ""

    def to_message_ru(self):
        message = (
            f"{self.full_name}\n"
            f"Страна: {self.country}\n"
            f"Широта: {self.latitude}\n"
            f"Долгота: {self.longitude}\n"
            f"Почтовый индекс: {self.post}\n"
            f"Телефонный код: {self.telcod}\n"
            f"Часовой пояс: {self.tz}\n"
            f"Название на английском: {self.full_english}\n"
            f"Ссылка на wiki: {self.wiki}\n"
        )
        return message

    def to_message_en(self):
        message = (
            f"{self.full_english}\n"
            f"Latitude: {self.latitude}\n"
            f"Longitude: {self.longitude}\n"
            f"Postcode: {self.post}\n"
            f"Telephone code: {self.telcod}\n"
            f"Timezone: {self.tz}\n"
            f"Link to wiki: {self.wiki}\n"
        )
        return message


class Country(BaseModel):
    name: str = ""
    fullname: str = ""
    english: str = ""
    id_country: str = ""
    country_code3: str = ""
    iso: int = 0
    telcod: int = 0
    telcod_len: int = 0
    location: str = ""
    capital: str = "Not Found"
    mcc: str = ""
    lang: str = ""
    langcod: str = ""

    def to_message_ru(self):
        if self.fullname == "":
            mes_name = f"{self.name}\n"
        else:
            mes_name = f"{self.fullname}\n"
        message = (
            f"Столица: {self.capital}\n"
            f"Местоположение: {self.location}\n"
            f"Язык: {self.lang}\n"
            f"Код страны: {self.id_country}\n"
            f"Телефонный код: {self.telcod}\n"
            f"Название на английском: {self.english}"
        )
        return mes_name + message

    def to_message_en(self):
        mes_name = f"{self.english}\n"
        message = (
            f"Location: {self.location}\n"
            f"Language: {self.lang}\n"
            f"Country code: {self.id_country}\n"
            f"Telephone code: {self.telcod}"
        )
        return mes_name + message


class Currency(BaseModel):
    Nominal: float
    Value: float
    Name: str
    CharCode: str

    def to_message_ru(self, code):
        if code == "RU":
            message = (
                f"Валюта: российский рубль\n"
                f"Код: RUB\n"
                f"1 RUB = {1 / self.Value} USD"
            )
        else:
            message = (
                f"Валюта: {self.Name}\n"
                f"Код: {self.CharCode}\n"
                f"{self.Nominal} {self.CharCode} = {self.Value} RUB"
            )
        return message

    def to_message_en(self, code):
        if code == "RU":
            message = (
                f"Currency: russian ruble\n"
                f"Code: RUB\n"
                f"1 RUB = {1 / self.Value} USD"
            )
        else:
            message = (
                f"Currency: {self.Name}\n"
                f"Code: {self.CharCode}\n"
                f"{self.Nominal} {self.CharCode} = {self.Value} RUB"
            )
        return message


class Weather(BaseModel):
    temp: float
    feels_like: float
    condition: str
    wind_speed: float
    wind_gust: float
    wind_dir: str
    pressure_mm: float
    humidity: float

    def to_message_ru(self):
        message = (
            f"{self.condition}\n"
            f"Температура: {self.temp} C\n"
            f"Ощущается как: {self.feels_like} C\n"
            f"Скорость ветра: {self.wind_speed} м/с\n"
            f"Порывы ветра: {self.wind_gust} м/с\n"
            f"Направление ветра: {self.wind_dir}\n"
            f"Давление: {self.pressure_mm} мм.рт.ст.\n"
            f"Влажность: {self.humidity}%"
        )
        return message

    def to_message_en(self):
        message = (
            f"Temperature: {self.temp} C\n"
            f"Feels like: {self.feels_like} C\n"
            f"Wind speed: {self.wind_speed} m/s\n"
            f"Gusts of wind: {self.wind_gust} m/s\n"
            f"Pressure: {self.pressure_mm} mm\n"
            f"Humidity: {self.humidity}%"
        )
        return message
