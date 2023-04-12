from core.HTTPclient import HTTPClient, HTTPError
from core.serializers import CurrencySerializer
from core.APICLients.InterfaceAPI import CurrencyExternalAPIInterface
from core.APICLients.currencyConstants import CURRENCIES


class CurrencyExternalAPIClient(CurrencyExternalAPIInterface):
    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    def get_currency(self, code) -> dict:
        if code not in CURRENCIES:
            raise HTTPError
        content, status = self._http_client.get("")
        if status != 200:
            raise HTTPError
        serializer = CurrencySerializer(data=content['Valute'][CURRENCIES[code]])
        if serializer.is_valid():
            return serializer.validated_data
        raise HTTPError
