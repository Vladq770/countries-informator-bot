from core.HTTPclient import HTTPClient, HTTPError
from core.serializers import WeatherSerializer
from core.APICLients.InterfaceAPI import WeatherExternalAPIInterface
from core.APICLients.weatherConstants import WIND_DIR, CONDITION


class WeatherExternalAPIClient(WeatherExternalAPIInterface):
    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_weather(self, latitude, longitude):
        params = {'params': {'lat': latitude, 'lon': longitude, 'extra': 'true'}}
        content, status = self._http_client.get("", **params)
        if status != 200:
            raise HTTPError
        serializer = WeatherSerializer(data=content['fact'])
        if serializer.is_valid():
            serializer.validated_data['condition'] = CONDITION[serializer.validated_data['condition']]
            serializer.validated_data['wind_dir'] = WIND_DIR[serializer.validated_data['wind_dir']]
            return serializer.validated_data
        raise HTTPError
