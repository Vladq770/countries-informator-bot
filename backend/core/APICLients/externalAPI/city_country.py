from core.HTTPclient import HTTPClient, HTTPError, logger
from core.serializers import CitySerializer, CountrySerializer
from core.APICLients.InterfaceAPI import CityExternalAPIInterface


class CityExternalAPIClient(CityExternalAPIInterface):
    def __init__(self, http_client: HTTPClient, token):
        self._http_client = http_client
        self._token = token

    def get_city(self, name) -> list[dict]:
        cities = []
        params = {'params': {'city_name': name, 'json': '', 'api_key': self._token}}
        content, status = self._http_client.get("", **params)
        if status != 200:
            raise HTTPError
        for i in range(len(content) - 2):
            data_city = content[str(i)]
            for k, v in data_city.items():
                if v is None or v == '':
                    data_city[k] = 'NF'
            code = data_city.pop('country')
            serializer = CitySerializer(data=data_city)
            if not serializer.is_valid():
                raise HTTPError
            data_city = serializer.validated_data
            data_city['country'] = code
            cities.append(data_city)
        return cities

    def get_country(self, name) -> dict:
        params = {'params': {'country': name, 'info': '', 'json': '', 'api_key': self._token}}
        content, status = self._http_client.get("", **params)
        if status != 200 or len(content) < 5:
            raise HTTPError
        data_country = content['country']
        serializer = CountrySerializer(data=data_country)
        if not serializer.is_valid():
            raise HTTPError
        data = serializer.validated_data
        data["id_country"] = data_country['id']
        if 'capital' in content:
            data["capital"] = content['capital']['name']
        return data
