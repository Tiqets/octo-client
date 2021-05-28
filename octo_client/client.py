from datetime import date
import logging
from typing import Callable, Dict, List

import requests

from octo_client import exceptions, models

logger = logging.getLogger('octo_client')
logger.setLevel(logging.INFO)


class OctoClient(object):
    """
    HTTP client for OCTo (Open Connection for Tourism) APIs.
    """

    def __init__(self, url: str, token: str, custom_logger: logging.Logger = None) -> None:
        self.url = url.rstrip('/')
        self.token = token
        self.logger = custom_logger or logger
        self.suppliers: List[models.Supplier] = []
        self.supplier_url_map: Dict[str, str] = {}
        self.requests_loglevel = logging.DEBUG
        self.log_responses = False

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
        if path.startswith('suppliers/'):
            supplier_id = path.split('/')[1]
            if not self.suppliers:
                self.get_suppliers()
            try:
                endpoint_url = self.supplier_url_map[supplier_id]
            except KeyError:
                raise exceptions.InvalidRequest('Incorrect supplierId')
            full_url = f'{endpoint_url}/{path}'
        else:
            full_url = f'{self.url}/{path}'
        self.logger.log(self.requests_loglevel, 'Sending request to %s (%s)', full_url, http_method.__name__.upper())
        response = http_method(
            full_url,
            params=params or {},
            json=json,
            headers=self._get_headers(),
        )
        self._raise_for_status(response.status_code, response.content)
        try:
            response_json = response.json()
        except Exception:
            raise exceptions.ApiError('Non-JSON response')
        self.logger.log(
            self.requests_loglevel,
            'Got response from %s (%s)',
            full_url,
            http_method.__name__.upper(),
            extra={"response": response_json} if self.log_responses else None
        )
        return response_json

    def _get_headers(self) -> Dict[str, str]:
        return {'Authorization': f'Bearer {self.token}'}

    def _http_get(self, path: str, params=None):
        return self._make_request(requests.get, path, params=params)

    def _http_post(self, path: str, json: dict, params=None):
        return self._make_request(requests.post, path, json=json, params=params)

    def _http_delete(self, path: str, params=None):
        return self._make_request(requests.delete, path, params=params)

    def get_suppliers(self) -> List[models.Supplier]:
        '''
        This list MAY be limited based on the suppliers that the authenticated user has been granted access to.
        '''
        response = self._http_get('suppliers')
        try:
            self.suppliers = [models.Supplier.from_dict(supplier) for supplier in response]
        except AttributeError:
            raise exceptions.ApiError(response)
        self.logger.info('Found %s suppliers', len(self.suppliers), extra={'suppliers': response})
        self.supplier_url_map = {
            supplier.id: supplier.endpoint for supplier in self.suppliers
        }
        return self.suppliers

    def get_products(self, supplier_id: str) -> List[models.Product]:
        '''
        Contains all product details necessary to ingest, map, and sell.
        '''
        response = self._http_get(f'suppliers/{supplier_id}/products')
        products = [models.Product.from_dict(product) for product in response]
        self.logger.info('Found %s products', len(products), extra={'products': products})
        return products

    def get_calendar(
        self,
        supplier_id: str,
        product_id: str,
        option_id: str,
        start_date: date,
        end_date: date,
        extra_fields: dict = None,
    ) -> List[models.AvailabilityCalendarItem]:
        '''
        Returns an availability for given product and option.
        '''
        params = {
            'productId': product_id,
            'optionId': option_id,
            'localDateStart': start_date.isoformat(),
            'localDateEnd': end_date.isoformat(),
        }
        if extra_fields:
            params.update(extra_fields)
        response = self._http_get(f'suppliers/{supplier_id}/availability/calendar', params=params)
        daily_availability = [models.AvailabilityCalendarItem.from_dict(availability) for availability in response]
        self.logger.info('Found %s days', len(daily_availability), extra={'calendar': response})
        return daily_availability

    def get_availability(
        self,
        supplier_id: str,
        product_id: str,
        option_id: str,
        start_date: date,
        end_date: date,
        extra_fields: dict = None,
    ) -> List[models.AvailabilityItem]:
        '''
        For any dates which are never available for booking, the response MUST exclude those dates entirely.

        If the product's availabilityType is OPENING_HOURS then the localDateTimeStart and localDateTimeEnd
        are the hours of operation. If a product has more than one hours of operation on the same day
        (e.g. the supplier is open 8-5 but closed for lunch from 12-1) then one availability object
        MUST be returned for each contiguous range of time for that day.

        The availability id value MUST be sent when making a Booking request.

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
        params = {
            'productId': product_id,
            'optionId': option_id,
            'localDateStart': start_date.isoformat(),
            'localDateEnd': end_date.isoformat(),
        }
        if extra_fields:
            params.update(extra_fields)
        response = self._http_get(f'suppliers/{supplier_id}/availability', params=params)
        detailed_availability = [models.AvailabilityItem.from_dict(availability) for availability in response]
        self.logger.info('Found %s items', len(detailed_availability), extra={'availability': response})
        return detailed_availability

    def test_availability(
        self,
        supplier_id: str,
        product_id: str,
        option_id: str,
        availability_ids: List[str],
        units: List[models.UnitQuantity],
        extra_fields: dict = None,
    ) -> List[models.AvailabilityItem]:
        '''
        This request is intended to provide the Booking Platform a complete view of the Unit IDs, Unit quantity,
        and Availability IDs so that additional restrictions and policies can be validated within
        the Booking Platform prior to making a Booking. The purpose is to provide a clear and accurate
        answer to the Reseller about whether the requested booking configuration could be accepted by the Supplier.
        This is to support complex booking requirements without the Reseller needing to know the details
        of the restriction (e.g. "must purchase at least 1 adult ticket if a child ticket is purchased").
        '''
        json_data = {
            'productId': product_id,
            'optionId': option_id,
            'availabilityIds': availability_ids,
            'units': [unit.as_dict() for unit in units],
        }
        if extra_fields:
            json_data.update(extra_fields)
        response = self._http_post(f'suppliers/{supplier_id}/availability', json=json_data)
        detailed_availability = [models.AvailabilityItem.from_dict(availability) for availability in response]
        self.logger.info('Found %s items', len(detailed_availability), extra={'availability': response})
        return detailed_availability

    def create_booking(
        self,
        supplier_id: str,
        booking_request: models.BookingRequest,
    ) -> models.Booking:
        '''
        This creates a new pending booking.

        This call has to be idempotent. To be able to safely retry a call on any network error or timeout,
        therefore it MUST not fail on retry or create a duplicate booking. The idempotency key is the UUID.
        A supplier SHOULD verify that a retried request with the same UUID is matching the original booking data,
        to avoid erroneous clients generating repeating UUIDs and response with the status 400
        and ErrorCode 1005 in such case.
        '''
        response = self._http_post(f'suppliers/{supplier_id}/bookings', json=booking_request.as_dict())
        self.logger.info('Booking created', extra={'booking': response})
        return models.Booking.from_dict(response)

    def confirm_booking(
        self,
        supplier_id: str,
        uuid: str,
        confirmation_request: models.BookingConfirmationRequest,
    ) -> models.Booking:
        '''
        This confirms an in-progress booking. The utcHoldExpiration MUST NOT be elapsed when this request is sent,
        otherwise the response MAY show a status of EXPIRED.

        This call MUST be idempotent so that a Reseller may retry the request for any network error or timeout.
        The Booking uuid MUST be used to ensure idempotency of the request.
        '''
        response = self._http_post(
            f'suppliers/{supplier_id}/bookings/{uuid}/confirm',
            json=confirmation_request.as_dict(),
        )
        self.logger.info('Booking confirmed', extra={'booking': response})
        return models.Booking.from_dict(response)

    def get_booking_details(self, supplier_id: str, uuid: str) -> models.Booking:
        '''
        This returns the current state of any valid booking. This request MAY be made at any point after
        the initial createBooking request is processed successfully and it MUST return the booking object.
        '''
        response = self._http_get(f'suppliers/{supplier_id}/bookings/{uuid}')
        self.logger.info('Got booking details', extra={'booking': response})
        return models.Booking.from_dict(response)

    def delete_booking(
        self,
        supplier_id: str,
        uuid: str,
        reason: models.CancelReason,
        reason_details: str,
        extra_fields: dict = None,
    ) -> models.Booking:
        '''
        This expires the availability hold of an in-progress booking so that the availablity is release
        for other bookings. This request is a courtesy, however Resellers SHOULD send this in order
        to ensure proper cleanup of any outstanding holds.

        This call has to be idempotent. To be able to safely retry a call on any network error or timeout,
        therefore it MUST not fail on retry. The idempotency key is the UUID.
        '''
        json_data = {
            'reason': reason.value,
            'reasonDetails': reason_details,
        }
        if extra_fields:
            json_data.update(extra_fields)
        response = self._http_post(f'suppliers/{supplier_id}/bookings/{uuid}/cancel', json=json_data)
        self.logger.info('Booking removed', extra={'booking': response})
        return models.Booking.from_dict(response)
