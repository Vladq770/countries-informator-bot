from core.HTTPclient import HTTPClient


class CityExternalAPIInterface:

    _http_client: HTTPClient

    def get_city(self, name) -> list[dict]:
        """Get cities from API"""

    def get_country(self, name) -> dict:
        """Get country from API"""


class CurrencyExternalAPIInterface:

    _http_client: HTTPClient

    def get_currency(self, code) -> dict:
        """Get currency from API"""


class WeatherExternalAPIInterface:

    _http_client: HTTPClient

    def get_weather(self, latitude, longitude) -> dict:
        """Get weather from API"""