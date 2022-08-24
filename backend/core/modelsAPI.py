from pydantic import BaseModel


class Country(BaseModel):
    name: str
    fullname: str = ''
    english: str = ''
    country_code3: str = ''
    iso: int = 0
    telcod: int = 0
    telcod_len: int = 0
    location: str = ''
    mcc: int = 0
    lang: str = ''
    langcod: str = ''
    time_zone: int = 0
    tz: str = ''


class City(BaseModel):
    name: str = ''
    area: int = 0
    telcod: str = ''
    latitude: str = ''
    longitude: str = ''
    time_zone: float = 0.0
    tz: str = ''
    english: str = ''
    rajon: int = 0
    sub_rajon: int = 0
    iso: str = ''
    vid: int = 0
    post: str = ''
    wiki: str = ''
    full_english: str = ''
    full_name: str = ''
    country: str = ''