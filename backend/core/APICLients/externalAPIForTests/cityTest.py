from core.HTTPclient import HTTPClient, HTTPError, logger
from core.serializers import CitySerializer, CountrySerializer
from core.APICLients.InterfaceAPI import CityExternalAPIInterface
from copy import deepcopy

TEST_CONTENT_CITY = {
    "0": {
        "name": "Тольятти",
        "country": "RU",
        "full_name": "Тольятти (Самарская область)",
        "tz": "Europe/Samara",
        "latitude": 53.5356,
        "longitude": 49.4096,
        "full_english": "Tol'yatti (Samara oblast)",
        "iso": "",
        "english": "Tol'yatti"
    },
    "1": "123",
    "2": "123"
}
TEST_CONTENT_COUNTRY = {
    "country": {
        "name": "Россия",
        "fullname": "Российская Федерация",
        "id": "RU",
        "english": "Russia"
    }
}


class CityExternalAPIClient(CityExternalAPIInterface):

    def __init__(self, http_client: HTTPClient, token):
        self._http_client = http_client
        self._token = token

    def get_city(self, name) -> list[dict]:
        cities = []
        content = deepcopy(TEST_CONTENT_CITY)
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
        content = deepcopy(TEST_CONTENT_COUNTRY)
        data_country = content['country']
        serializer = CountrySerializer(data=data_country)
        if not serializer.is_valid():
            raise HTTPError
        data = serializer.validated_data
        data["id_country"] = data_country['id']
        if 'capital' in content:
            data["capital"] = content['capital']['name']
        return data
