import logging
from typing import Callable, Dict, List, Union

import requests

from icf_client import exceptions, models

logger = logging.getLogger('icf_client')


class IcfClient(object):
    """
    HTTP client for API standard developed by the Independent Connectivity Forum.
    """

    def __init__(self, url: str, token: str) -> None:
        self.url = url.rstrip('/')
        self.token = token

    @staticmethod
    def _raise_for_status(status_code: int) -> None:
        CODE_EXCEPTION_MAP = {
            400: exceptions.InvalidRequest,
            403: exceptions.Unauthorized,
            404: exceptions.ApiError,
            500: exceptions.ApiError,
        }
        if status_code in CODE_EXCEPTION_MAP:
            raise CODE_EXCEPTION_MAP[status_code]()

    def _make_request(self, http_method: Callable, path: str) -> dict:
        full_url = f'{self.url}/{path}'
        logger.debug('%s %s', http_method.__name__.upper(), full_url)
        response = http_method(full_url, headers=self._get_headers())
        self._raise_for_status(response.status_code)
        return response.json()

    def _get_headers(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.token}'}

    def _http_get(self, path: str) -> Union[dict, list]:
        return self._make_request(requests.get, path)

    def get_suppliers(self) -> List[models.Supplier]:
        suppliers = [models.Supplier.from_dict(supplier) for supplier in self._http_get('suppliers')]
        logger.debug('Found %s suppliers', len(suppliers))
        return suppliers
