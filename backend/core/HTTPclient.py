import logging
import sys
from json import JSONDecodeError
from typing import Any, Optional
from urllib.parse import urljoin
import backoff
import httpx
from httpx import codes, ConnectTimeout


def get_logger(level: str = logging.DEBUG):
    _logger = logging.getLogger("solution_logger")
    _logger.setLevel(level)
    handler = logging.StreamHandler(stream=sys.stdout)
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
    _logger.addHandler(handler)
    return _logger


logger = get_logger()


class HTTPSettingsInterface:
    HTTP_MAX_TRIES: int
    HTTP_MAX_TIME: int
    HTTP_TIMEOUT: int
    HTTP_LIMIT_MAX_CONN: int


class DefaultHTTPSettings(HTTPSettingsInterface):
    HTTP_MAX_TRIES = 5
    HTTP_MAX_TIME = 10
    HTTP_TIMEOUT = 10
    HTTP_LIMIT_MAX_CONN = 5


class HTTPClient:
    def __init__(
            self,
            base_url: str, http_settings: Optional[HTTPSettingsInterface] = DefaultHTTPSettings(),
            extra_request_params: Optional[dict] = None
    ):
        self._base_url = base_url
        self._httpx_client = httpx.Client(
            timeout=httpx.Timeout(http_settings.HTTP_TIMEOUT),
            limits=httpx.Limits(max_connections=http_settings.HTTP_LIMIT_MAX_CONN)
        )
        self._retry_policy = backoff.on_exception(
            backoff.expo,
            exception=BaseException,
            max_tries=http_settings.HTTP_MAX_TRIES,
            max_time=http_settings.HTTP_MAX_TIME
        )
        self._extra_request_params = extra_request_params or {}

    def get(self, endpoint_path: str, **request_params) -> Any:
        return self._request("GET", endpoint_path, **request_params)

    def post(self, endpoint_path: str, **request_params) -> Any:
        return self._request("POST", endpoint_path, **request_params)

    def _request(self, method: str, endpoint_path: str, **request_params: dict) -> tuple[Any, codes]:
        url: str = urljoin(self._base_url, endpoint_path)
        request_params = {**request_params, **self._extra_request_params}
        logger.debug(f"Request: {method} {endpoint_path} {url} {request_params}")
        try:
            response: httpx.Response = self._retry_policy(self._httpx_client.request)(method, url, **request_params)
        except ConnectTimeout:
            logger.error(f"Connect Timeout")
            return "", codes(500)
        try:
            content = response.json()
        except JSONDecodeError:
            content = response.text

        logger.debug(f"Response: Code: {codes(response.status_code)} {content}")
        return content, codes(response.status_code)


class HTTPError(BaseException):
    ...
