from HTTPClient import HTTPClient, HTTPError


class ExternalAPIInterface:

    _http_client: HTTPClient

    async def get_country(self, name) -> dict:
        """Get country from backend"""

    async def get_city(self, name) -> dict:
        """Get city from backend"""

    async def get_weather(self, latitude, longitude) -> dict:
        """Get weather from backend"""

    async def get_currency(self, code) -> dict:
        """Get currency from backend"""


class ExternalAPIClient:

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    async def get_currency(self, code) -> dict:
        data, status = await self._http_client.get(f"core/currency/{code}/")
        if status == 200:
            return data
        raise HTTPError

    async def get_weather(self, latitude, longitude) -> dict:
        data, status = await self._http_client.get(f"core/weather/{latitude}/{longitude}/")
        if status == 200:
            return data
        raise HTTPError

    async def get_country(self, name) -> dict:
        data, status = await self._http_client.get(f"core/country/{name}")
        if status == 200:
            return data
        raise HTTPError

    async def get_city(self, name) -> dict:
        data, status = await self._http_client.get(f"core/city/{name}")
        if status == 200:
            return data
        raise HTTPError
