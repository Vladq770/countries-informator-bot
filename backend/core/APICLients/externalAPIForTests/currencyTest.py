from core.HTTPclient import HTTPClient, HTTPError
from core.serializers import CurrencySerializer
from core.APICLients.InterfaceAPI import CurrencyExternalAPIInterface
from core.APICLients.currencyConstants import CURRENCIES


TEST_CONTENT = {
    "Valute": {
        "USD": {
            "Nominal": 1.0,
            "Value": 59.6663,
            "Name": "Доллар США",
            "CharCode": "USD"
        }
    }
}


class CurrencyExternalAPIClient(CurrencyExternalAPIInterface):
    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_currency(self, code) -> dict:
        content = TEST_CONTENT
        serializer = CurrencySerializer(data=content['Valute'][CURRENCIES[code]])
        if serializer.is_valid():
            return serializer.validated_data
        raise HTTPError
