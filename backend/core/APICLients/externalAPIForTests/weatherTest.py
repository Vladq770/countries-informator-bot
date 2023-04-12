from core.HTTPclient import HTTPClient, HTTPError
from core.serializers import WeatherSerializer
from core.APICLients.InterfaceAPI import WeatherExternalAPIInterface
from core.APICLients.weatherConstants import WIND_DIR, CONDITION


TEST_CONTENT = {
    "fact": {
        "temp": 13.4,
        "feels_like": 11.7,
        "condition": "clear",
        "wind_speed": 4.3,
        "wind_gust": 7.2,
        "wind_dir": "nw",
        "pressure_mm": 745.2,
        "humidity": 57.2
    }
}


class WeatherExternalAPIClient(WeatherExternalAPIInterface):
    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_weather(self, latitude, longitude):
        content = TEST_CONTENT
        serializer = WeatherSerializer(data=content['fact'])
        if serializer.is_valid():
            serializer.validated_data['condition'] = CONDITION[serializer.validated_data['condition']]
            serializer.validated_data['wind_dir'] = WIND_DIR[serializer.validated_data['wind_dir']]
            return serializer.validated_data
        raise HTTPError
