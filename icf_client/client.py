from datetime import date
import logging
from typing import Callable, Dict, List

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
    def _raise_for_status(status_code: int, response_content: str) -> None:
        CODE_EXCEPTION_MAP = {
            400: exceptions.InvalidRequest,
            403: exceptions.Unauthorized,
            404: exceptions.ApiError,
            500: exceptions.ApiError,
        }
        if status_code in CODE_EXCEPTION_MAP:
            raise CODE_EXCEPTION_MAP[status_code](response_content)

    def _make_request(self, http_method: Callable, path: str, json=None, params=None):
        full_url = f'{self.url}/{path}'
        logger.debug('%s %s', http_method.__name__.upper(), full_url)
        response = http_method(
            full_url,
            params=params or {},
            json=json or {},
            headers=self._get_headers(),
        )
        self._raise_for_status(response.status_code, response.content)
        return response.json()

    def _get_headers(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.token}'}

    def _http_get(self, path: str, params=None):
        return self._make_request(requests.get, path, params=params)

    def _http_post(self, path: str, json: dict, params=None):
        return self._make_request(requests.post, path, json=json, params=params)

    def _http_put(self, path: str, json: dict, params=None):
        return self._make_request(requests.put, path, json=json, params=params)

    def get_suppliers(self) -> List[models.Supplier]:
        '''
        This list MAY be limited based on the suppliers that the authenticated user has been granted access to.
        '''
        response = self._http_get('suppliers')
        suppliers = [models.Supplier.from_dict(supplier) for supplier in response]
        logger.debug('Found %s suppliers', len(suppliers))
        return suppliers

    def get_products(self, supplier_id: str) -> List[models.Product]:
        '''
        Contains all product details necessary to ingest, map, and sell.
        '''
        response = self._http_get('products', params={'supplierId': supplier_id})
        products = [models.Product.from_dict(product) for product in response]
        logger.debug('Found %s products', len(products))
        return products

    def get_calendar(
        self,
        supplier_id: str,
        product_id: str,
        start_date: date,
        end_date: date
    ) -> List[models.DailyAvailability]:
        response = self._http_get('calendar', params={
            'supplierId': supplier_id,
            'productId': product_id,
            'localDateStart': start_date.isoformat(),
            'localDateEnd': end_date.isoformat(),
        })
        daily_availability = [models.DailyAvailability.from_dict(availability) for availability in response]
        logger.debug('Found %s days', len(daily_availability))
        return daily_availability

    def get_availability(
        self,
        supplier_id: str,
        product_id: str,
        option_id: str,
        start_date: date,
        end_date: date,
    ) -> List[models.TimeslotAvailability]:
        '''
        For any dates which are never available for booking, the response MUST exclude those dates entirely.

        If the product's availabilityType is OPENING_HOURS then the localStartDateTime and localEndDateTime
        are the hours of operation. If a product has more than one hours of operation on the same day
        (e.g. the supplier is open 8-5 but closed for lunch from 12-1) then one availability object
        MUST be returned for each contiguous range of time for that day.

        The availability id value MUST be sent when making a Reservation request.

        The status field SHOULD be used to infer how frequently your cache should be updated from
        the Booking Platform. The RECOMMENDED frequency is as follows:

        FREESALE: Always available. Refresh no more than once/week.
        AVAILABLE: Currently available for sale, but has a fixed capacity. Refresh every 12 hours.
        LIMITED: Currently available for sale, but has a fixed capacity and may be sold out soon.
                    Refresh at least once/hour.
        SOLD_OUT: Currently sold out, but additional availability may free up. Refresh no more
                    than once/hour.
        CLOSED: Currently not available for sale, but not sold out (e.g. temporarily on stop-sell)
                and may be available for sale soon. Refresh no more than once/12 hours.

        '''
        response = self._http_get('availability', params={
            'supplierId': supplier_id,
            'productId': product_id,
            'optionId': option_id,
            'localDateStart': start_date.isoformat(),
            'localDateEnd': end_date.isoformat(),
        })
        detailed_availability = [models.TimeslotAvailability.from_dict(availability) for availability in response]
        logger.debug('Found %s items', len(detailed_availability))
        return detailed_availability

    def test_reservation(
        self,
        supplier_id: str,
        product_id: str,
        option_id: str,
        availability_ids: List[str],
        units: List[models.UnitQuantity],
    ) -> List[models.TimeslotAvailability]:
        '''
        This request is intended to provide the Booking Platform a complete view of the Unit IDs,
        Unit quantity, and Availability IDs so that additional restrictions and policies can be
        validated within the Booking Platform prior to making a Reservation. The purpose is to
        provide a clear and accurate answer to the Reseller about whether the requested booking
        configuration could be accepted by the Supplier. This is to support complex booking
        requirements without the Reseller needing to know the details of the restriction
        (e.g. "must purchase at least 1 adult ticket if a child ticket is purchased").
        '''
        response = self._http_post('availability', params={'supplierId': supplier_id}, json={
            'productId': product_id,
            'optionId': option_id,
            'availabilityIds': availability_ids,
            'units': [unit.as_dict() for unit in units],
        })
        detailed_availability = [models.TimeslotAvailability.from_dict(availability) for availability in response]
        logger.debug('Found %s items', len(detailed_availability))
        return detailed_availability

    def create_reservation(
        self,
        supplier_id: str,
        reservation_request: models.ReservationRequest,
    ) -> models.Reservation:
        '''
        This creates a new booking reservation.
        '''
        response = self._http_post(
            'reservations',
            params={'supplierId': supplier_id},
            json=reservation_request.as_dict(),
        )
        logger.debug('Reservation created')
        return models.Reservation.from_dict(response)

    def confirm_reservation(
        self,
        supplier_id: str,
        confirmation_request: models.ReservationConfirmationRequest,
    ) -> models.Reservation:
        '''
        This confirms an existing reservation. The utcHoldExpiration MUST NOT be elapsed when this request
        is sent, otherwise the response MAY show a status of EXPIRED.
        '''
        response = self._http_put(
            'reservations',
            params={'supplierId': supplier_id},
            json=confirmation_request.as_dict(),
        )
        logger.debug('Reservation confirmed')
        return models.Reservation.from_dict(response)
