import copy
import logging
from datetime import date
from typing import Any, Callable, Dict, List, Optional, Union

import requests

from octo_client import exceptions, models
from octo_client.utils import hide_sensitive_data

logger = logging.getLogger("octo_client")
logger.setLevel(logging.INFO)


class OctoClient(object):
    """
    HTTP client for OCTo (Open Connection for Tourism) APIs.
    """

    def __init__(
        self,
        url: str,
        token: str,
        custom_logger: Optional[logging.Logger] = None,
        log_size_limit: Optional[int] = None,
        requests_loglevel: int = logging.DEBUG,
        language: str = "en",
        strict: bool = False,
    ) -> None:
        """
        Args:
            url (str): URL under which the OCTO interface is available
            token (str): secret bearer token for the authorization
            custom_logger (Logger): custom logger which the client will use for logging
            log_size_limit (int): max limit of the log size above which the log will be truncated
            requests_loglevel (int): default log level that will be used to log requests and
                                     responses
            language (str): language that will be used in the Accept-Language header of each request
            strict (bool): in the strict mode client will raise an error if the response will
                           contain any additional data outside of the data model provided
                           by the specification
        """
        self.url = url.rstrip("/")
        self.token = token
        self.logger = custom_logger or logger
        self.supplier_url_map: Dict[str, str] = {}
        self.requests_loglevel = requests_loglevel
        self.log_responses = False
        self.log_requests = False
        self.log_size_limit = log_size_limit
        self.language = language
        self.strict = strict

    @staticmethod
    def _raise_for_status(status_code: int, response_text: str) -> None:
        CODE_EXCEPTION_MAP = {
            400: exceptions.InvalidRequest,
            403: exceptions.Unauthorized,
            404: exceptions.ApiError,
            500: exceptions.ApiError,
        }
        if status_code in CODE_EXCEPTION_MAP:
            raise CODE_EXCEPTION_MAP[status_code](response_text)

    def _build_endpoint_url_for_request(self, supplier_id: str, path: str) -> str:
        """Builds the endpoint's URL for making requests to a given supplier.

        Args:
            supplier_id: builds the URL for a supplier with this ID.
            path: use this path to build the URL.

        Returns: the full URL.
        Raises:
            - `exceptions.InvalidRequest` if the supplier ID is unknown.

        """

        if supplier_id not in self.supplier_url_map:
            self.get_suppliers()

        try:
            endpoint_url = self.supplier_url_map[supplier_id]
        except KeyError as e:
            raise exceptions.InvalidRequest("Incorrect supplierId") from e

        cleaned_endpoint = endpoint_url.rstrip("/")

        return cleaned_endpoint if cleaned_endpoint.endswith(path) else f"{cleaned_endpoint}/{path}"

    def _make_request(
        self,
        http_method: Callable,
        path: str,
        supplier_id=None,
        json: Optional[Dict] = None,
        params=None,
        headers: Optional[Dict] = None,
    ):
        if headers is None:
            headers = {}

        if params is None:
            params = {}

        full_url: str = (
            self._build_endpoint_url_for_request(str(supplier_id), path)
            if supplier_id
            else f"{self.url}/{path}"
        )

        request_log_data: dict = {"json": json, "params": params}

        self.logger.log(
            self.requests_loglevel,
            "Sending request to %s (%s)",
            full_url,
            http_method.__name__.upper(),
            extra={"request": self._filter_request_log_data(request_log_data)},
        )
        base_headers = self._get_headers()
        headers = {**base_headers, **headers}
        response = http_method(
            full_url,
            params=params,
            json=json,
            headers=headers,
        )
        self._raise_for_status(response.status_code, response.text)
        try:
            response_json: dict = response.json()
        except Exception as exc:
            self.logger.log(
                self.requests_loglevel,
                "Received non-JSON response",
                extra={"response": self._filter_response_log_data(response.text)},
            )
            raise exceptions.ApiError("Non-JSON response") from exc
        self.logger.log(
            self.requests_loglevel,
            "Got response from %s (%s)",
            full_url,
            http_method.__name__.upper(),
            extra={"response": self._filter_response_log_data(response_json)},
        )
        return response_json

    def _filter_request_log_data(
        self, request_content: Union[str, dict, list]
    ) -> Optional[Union[str, dict, list]]:
        if self.log_requests:
            content = hide_sensitive_data(copy.deepcopy(request_content))
            if self.log_size_limit and len(content) > self.log_size_limit:
                return "TRUNCATED"
            return content
        return None

    def _filter_response_log_data(
        self, response_content: Union[str, dict, list]
    ) -> Optional[Union[str, dict, list]]:
        if self.log_responses:
            content = hide_sensitive_data(copy.deepcopy(response_content))
            if self.log_size_limit and len(content) > self.log_size_limit:
                return "TRUNCATED"
            return content
        return None

    def _get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept-Language": self.language,
        }

    def _http_get(
        self,
        path: str,
        supplier_id: Optional[str] = None,
        params=None,
        headers: Optional[Dict] = None,
    ):
        return self._make_request(
            requests.get, path, supplier_id=supplier_id, params=params, headers=headers
        )

    def _http_post(
        self, path: str, json: dict, supplier_id: str, params=None, headers: Optional[Dict] = None
    ):
        if headers is None:
            headers = {}
        return self._make_request(
            requests.post,
            path,
            json=json,
            supplier_id=supplier_id,
            params=params,
            headers={"Content-Type": "application/json", **headers},
        )

    def _http_patch(
        self, path: str, json: dict, supplier_id: str, params=None, headers: Optional[Dict] = None
    ):
        if headers is None:
            headers = {}
        return self._make_request(
            requests.patch,
            path,
            json=json,
            supplier_id=supplier_id,
            params=params,
            headers={"Content-Type": "application/json", **headers},
        )

    def _http_delete(
        self, path: str, supplier_id: str, json: dict, params=None, headers: Optional[Dict] = None
    ):
        if headers is None:
            headers = {}
        return self._make_request(
            requests.delete,
            path,
            supplier_id=supplier_id,
            json=json,
            params=params,
            headers={"Content-Type": "application/json", **headers},
        )

    def get_supplier(self, supplier_id: str, headers: Optional[Dict] = None) -> models.Supplier:
        response = self._http_get(
            f"suppliers/{supplier_id}", supplier_id=supplier_id, headers=headers
        )
        try:
            supplier = models.Supplier.from_dict(response, strict=self.strict)
        except AttributeError as e:
            raise exceptions.ApiError(response) from e
        return supplier

    def get_suppliers(self, headers: Optional[Dict] = None) -> List[models.Supplier]:
        response = self._http_get("suppliers", headers=headers)
        try:
            suppliers = [
                models.Supplier.from_dict(supplier, strict=self.strict) for supplier in response
            ]
        except AttributeError as e:
            raise exceptions.ApiError(response) from e
        self.logger.info("Found %s suppliers", len(suppliers), extra={"suppliers": response})
        self.supplier_url_map = {supplier.id: supplier.endpoint for supplier in suppliers}
        return suppliers

    def get_products(
        self, supplier_id: str, headers: Optional[Dict] = None
    ) -> List[models.Product]:
        response = self._http_get("products", supplier_id=supplier_id, headers=headers)
        products = [models.Product.from_dict(product, strict=self.strict) for product in response]
        self.logger.info("Found %s products", len(products), extra={"products": products})
        return products

    def get_product(
        self, supplier_id: str, product_id: str, headers: Optional[Dict] = None
    ) -> models.Product:
        response = self._http_get(
            f"products/{product_id}", supplier_id=supplier_id, headers=headers
        )
        return models.Product.from_dict(response, strict=self.strict)

    def availability_check(
        self,
        supplier_id: str,
        product_id: str,
        option_id: str,
        units: Optional[List[models.UnitQuantity]] = None,
        local_date_start: Optional[date] = None,
        local_date_end: Optional[date] = None,
        local_date: Optional[date] = None,
        availability_ids: Optional[List[str]] = None,
        headers: Optional[Dict] = None,
    ) -> List[models.Availability]:
        payload: Dict[str, Any] = {
            "productId": product_id,
            "optionId": option_id,
        }
        if any([local_date_start, local_date_end]) and not all([local_date_start, local_date_end]):
            raise ValueError("local_date_start and local_date_end needs to be used together")
        if local_date_start:
            payload["localDateStart"] = local_date_start.isoformat()
        if local_date_end:
            payload["localDateEnd"] = local_date_end.isoformat()
        if local_date:
            payload["localDate"] = local_date.isoformat()
        if availability_ids:
            payload["availabilityIds"] = availability_ids
        if units:
            payload["units"] = [unit.as_dict() for unit in units]

        response = self._http_post(
            "availability", supplier_id=supplier_id, json=payload, headers=headers
        )
        detailed_availability = [
            models.Availability.from_dict(availability, strict=self.strict)
            for availability in response
        ]
        self.logger.info("Found %s items", len(detailed_availability))
        return detailed_availability

    def get_calendar(
        self,
        supplier_id: str,
        product_id: str,
        option_id: str,
        local_date_start: date,
        local_date_end: date,
        units: Optional[List[models.UnitQuantity]] = None,
        headers: Optional[Dict] = None,
    ) -> List[models.AvailabilityCalendarItem]:
        """This method retrieve the availability calendar for a range of dates.

        Args:
            supplier_id: retrieve calendar data for the supplier with this ID.
            product_id: retrieve calendar data for a product with this ID.
            option_id: retrieve calendar data for the option with this ID.
            local_date_start: retrieve calendar data from this date onwards.
            local_date_end: retrieve calendar data until this date.
            units: a list of units. Each unit requires:
                - id
                - quantity
            headers: optional HTTP headers to send in the request.

        Returns: a list of availability objects; one object per each day in the range of dates.
        """

        payload: Dict[str, Any] = {
            "productId": product_id,
            "optionId": option_id,
        }
        if local_date_start:
            payload["localDateStart"] = local_date_start.isoformat()
        if local_date_end:
            payload["localDateEnd"] = local_date_end.isoformat()
        if units:
            payload["units"] = [unit.as_dict() for unit in units]

        response = self._http_post(
            "availability/calendar", supplier_id=supplier_id, json=payload, headers=headers
        )
        daily_availability = [
            models.AvailabilityCalendarItem.from_dict(availability, strict=self.strict)
            for availability in response
        ]
        self.logger.info("Found %s days", len(daily_availability))
        return daily_availability

    def booking_reservation(
        self,
        supplier_id: str,
        uuid: str,
        product_id: str,
        option_id: str,
        availability_id: str,
        unit_items: List[models.UnitItem],
        expiration_minutes: Optional[int] = None,
        notes: Optional[str] = None,
        headers: Optional[Dict] = None,
    ) -> models.Booking:
        payload: Dict[str, Any] = {
            "uuid": uuid,
            "productId": product_id,
            "optionId": option_id,
            "availabilityId": availability_id,
            "unitItems": [unit.as_dict() for unit in unit_items],
        }
        if expiration_minutes:
            payload["expirationMinutes"] = expiration_minutes
        if notes:
            payload["notes"] = notes
        response = self._http_post(
            "bookings",
            supplier_id=supplier_id,
            json=payload,
            headers=headers,
        )
        self.logger.info("Booking created", extra={"booking": response})
        return models.Booking.from_dict(response)

    def list_bookings(
        self,
        supplier_id: str,
        reseller_reference: Optional[str] = None,
        supplier_reference: Optional[str] = None,
        local_date: Optional[date] = None,
        local_date_start: Optional[date] = None,
        local_date_end: Optional[date] = None,
        headers: Optional[Dict] = None,
    ) -> List[models.Booking]:
        if not any(
            [reseller_reference, supplier_reference, local_date, local_date_start or local_date_end]
        ):
            raise ValueError("One of the query parameters has to be provided.")

        if any([local_date_start, local_date_end]) and not all([local_date_start, local_date_end]):
            raise ValueError("local_date_start and local_date_end needs to be used together")

        params: Dict[str, str] = {}
        if reseller_reference:
            params["resellerReference"] = reseller_reference
        elif supplier_reference:
            params["supplierReference"] = supplier_reference
        elif local_date:
            params["localDate"] = local_date.isoformat()
        elif local_date_start and local_date_end:
            params["localDateStart"] = local_date_start.isoformat()
            params["localDateEnd"] = local_date_end.isoformat()

        response = self._http_get(
            "bookings", supplier_id=supplier_id, params=params, headers=headers
        )
        return [models.Booking.from_dict(booking) for booking in response]

    def get_booking(
        self,
        supplier_id: str,
        uuid: str,
        headers: Optional[Dict] = None,
    ) -> models.Booking:
        response = self._http_get(f"bookings/{uuid}", supplier_id=supplier_id, headers=headers)
        return models.Booking.from_dict(response)

    def booking_confirmation(
        self,
        supplier_id: str,
        uuid: str,
        email_receipt: bool = False,
        reseller_reference: Optional[str] = None,
        contact_full_name: Optional[str] = None,
        contact_first_name: Optional[str] = None,
        contact_last_name: Optional[str] = None,
        contact_email_address: Optional[str] = None,
        contact_phone_number: Optional[str] = None,
        contact_locales: Optional[List[str]] = None,
        contact_postal_code: Optional[str] = None,
        contact_country: Optional[str] = None,
        contact_notes: Optional[str] = None,
        unit_items: Optional[List[models.ConfirmationUnitItem]] = None,
        headers: Optional[Dict] = None,
    ) -> models.Booking:
        payload: Dict[str, Any] = {}
        if email_receipt:
            payload["emailReceipt"] = email_receipt
        if reseller_reference:
            payload["resellerReference"] = reseller_reference
        if any(
            [
                contact_full_name,
                contact_first_name,
                contact_last_name,
                contact_email_address,
                contact_phone_number,
                contact_locales,
                contact_postal_code,
                contact_country,
                contact_notes,
            ]
        ):
            payload["contact"] = models.BookingContact.from_dict(
                {
                    "locales": contact_locales or [],
                    "fullName": contact_full_name,
                    "firstName": contact_first_name,
                    "lastName": contact_last_name,
                    "emailAddress": contact_email_address,
                    "phoneNumber": contact_phone_number,
                    "postalCode": contact_postal_code,
                    "country": contact_country,
                    "notes": contact_notes,
                }
            ).as_dict()
        if unit_items:
            payload["unitItems"] = [unit_item.as_dict() for unit_item in unit_items]

        response = self._http_post(
            f"bookings/{uuid}/confirm", supplier_id=supplier_id, json=payload, headers=headers
        )
        return models.Booking.from_dict(response)

    def extend_reservation(
        self,
        supplier_id: str,
        uuid: str,
        expiration_minutes: int,
        headers: Optional[Dict] = None,
    ) -> models.Booking:
        payload = {"expirationMinutes": expiration_minutes}
        response = self._http_post(
            f"bookings/{uuid}/extend", supplier_id=supplier_id, json=payload, headers=headers
        )
        return models.Booking.from_dict(response)

    def booking_cancellation(
        self,
        supplier_id: str,
        uuid: str,
        reason: Optional[str] = None,
        force: Optional[bool] = False,
        headers: Optional[Dict] = None,
    ) -> models.Booking:
        payload: Dict[str, Any] = {}
        if reason:
            payload["reason"] = reason
        if force:
            payload["force"] = force
        response = self._http_delete(
            f"bookings/{uuid}", supplier_id=supplier_id, json=payload, headers=headers
        )
        return models.Booking.from_dict(response)

    def booking_update(
        self,
        supplier_id: str,
        uuid: str,
        product_id: Optional[str] = None,
        option_id: Optional[str] = None,
        availability_id: Optional[str] = None,
        notes: Optional[str] = None,
        email_receipt: bool = False,
        reseller_reference: Optional[str] = None,
        contact_full_name: Optional[str] = None,
        contact_first_name: Optional[str] = None,
        contact_last_name: Optional[str] = None,
        contact_email_address: Optional[str] = None,
        contact_phone_number: Optional[str] = None,
        contact_locales: Optional[List[str]] = None,
        contact_postal_code: Optional[str] = None,
        contact_country: Optional[str] = None,
        contact_notes: Optional[str] = None,
        unit_items: Optional[List[models.ConfirmationUnitItem]] = None,
        headers: Optional[Dict] = None,
    ):
        payload: Dict[str, Any] = {}
        if product_id:
            payload["productId"] = product_id
        if option_id:
            payload["optionId"] = option_id
        if availability_id:
            payload["availabilityId"] = availability_id
        if notes:
            payload["notes"] = notes
        if email_receipt:
            payload["emailReceipt"] = email_receipt
        if reseller_reference:
            payload["resellerReference"] = reseller_reference

        if any(
            [
                contact_full_name,
                contact_first_name,
                contact_last_name,
                contact_email_address,
                contact_phone_number,
                contact_locales,
                contact_postal_code,
                contact_country,
                contact_notes,
            ]
        ):
            payload["contact"] = {}
            if contact_locales:
                payload["contact"]["locales"] = contact_locales or []
            if contact_full_name:
                payload["contact"]["fullName"] = contact_full_name
            if contact_first_name:
                payload["contact"]["firstName"] = contact_first_name
            if contact_last_name:
                payload["contact"]["lastName"] = contact_last_name
            if contact_email_address:
                payload["contact"]["emailAddress"] = contact_email_address
            if contact_phone_number:
                payload["contact"]["phoneNumber"] = contact_phone_number
            if contact_postal_code:
                payload["contact"]["postalCode"] = contact_postal_code
            if contact_country:
                payload["contact"]["country"] = contact_country
            if contact_notes:
                payload["contact"]["notes"] = contact_notes

        if unit_items:
            payload["unitItems"] = [unit_item.as_dict() for unit_item in unit_items]

        response = self._http_patch(
            f"bookings/{uuid}", supplier_id=supplier_id, json=payload, headers=headers
        )
        return models.Booking.from_dict(response)
