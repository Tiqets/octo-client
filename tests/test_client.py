from datetime import date, datetime, timedelta, timezone
import json

import responses

from octo_client import OctoClient
from octo_client import models as m

BOOKING_JSON = {
    'uuid': 'f149068e-300e-452a-a856-3f091239f1d7',
    'resellerReference': '001-002',
    'supplierReference': 'ABC-123',
    'status': 'ON_HOLD',
    'utcHoldExpiration': '2019-10-31T08:30:00Z',
    'utcConfirmedAt': '2019-10-31T08:30:00Z',
    'utcDeliveredAt': '2019-10-31T08:30:00Z',
    'refreshFrequency': 'HOURLY',
    'productId': 'adult',
    'optionId': 'LR1-01',
    'availability': {
        'id': '28271273-a317-40fc-8f42-79725a7072a3',
        'localDateTimeStart': '2019-10-31T08:30:00Z',
        'localDateTimeEnd': '2019-10-31T10:00:00Z'
    },
    'contact': {
        'fullName': 'Mr. Traveller',
        'emailAddress': 'traveller@fake.com',
        'phoneNumber': '+1 555-555-1212',
        'locales': [
            'en-GB',
            'en-US',
            'en'
        ],
        'country': 'GB'
    },
    'deliveryMethods': [
        'VOUCHER'
    ],
    'voucher': {
        'deliveryOptions': [
            {
                'deliveryFormat': 'CODE39',
                'deliveryValue': '01234567890',
            }
        ],
        'redemptionMethod': 'DIGITAL',
        'utcDeliveredAt': '2019-10-31T08:30:00Z',
        'utcRedeemedAt': '2019-10-31T08:30:00Z'
    },
    'unitItems': [
        {
            'uuid': '6be0409f-181e-4520-acc1-cc6791896859',
            'unitId': 'adult',
            'resellerReference': '001-002',
            'supplierReference': 'ABC-123',
            'ticket': {
                'deliveryOptions': [
                    {
                        'deliveryFormat': 'CODE39',
                        'deliveryValue': '01234567890',
                    }
                ],
                'redemptionMethod': 'DIGITAL',
                'utcDeliveredAt': '2019-10-31T08:30:00Z',
                'utcRedeemedAt': '2019-10-31T08:30:00Z'
            }
        }
    ],
}
BOOKING_MODEL = m.Booking.from_dict({
    'uuid': 'f149068e-300e-452a-a856-3f091239f1d7',
    'status': 'ON_HOLD',
    'utcHoldExpiration': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
    'utcConfirmedAt': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
    'utcDeliveredAt': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
    'productId': 'adult',
    'optionId': 'LR1-01',
    'availability': {
        'id': '28271273-a317-40fc-8f42-79725a7072a3',
        'localDateTimeStart': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
        'localDateTimeEnd': datetime(2019, 10, 31, 10, 0, tzinfo=timezone.utc).isoformat(),
    },
    'contact': {
        'fullName': 'Mr. Traveller',
        'emailAddress': 'traveller@fake.com',
        'phoneNumber': '+1 555-555-1212',
        'locales': ['en-GB', 'en-US', 'en'],
        'country': 'GB'
    },
    'deliveryMethods': ['VOUCHER'],
    'voucher': {
        'deliveryOptions': [
            {
                'deliveryFormat': 'CODE39',
                'deliveryValue': '01234567890',
            }
        ],
        'redemptionMethod': 'DIGITAL',
        'utcDeliveredAt': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
        'utcRedeemedAt': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
    },
    'unitItems': [
        {
            'uuid': '6be0409f-181e-4520-acc1-cc6791896859',
            'unitId': 'adult',
            'ticket': {
                'deliveryOptions': [
                    {
                        'deliveryFormat': 'CODE39',
                        'deliveryValue': '01234567890',
                    }
                ],
                'redemptionMethod': 'DIGITAL',
                'utcDeliveredAt': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
                'utcRedeemedAt': datetime(2019, 10, 31, 8, 30, tzinfo=timezone.utc).isoformat(),
            },
            'resellerReference': '001-002',
            'supplierReference': 'ABC-123'
        }
    ],
    'resellerReference': '001-002',
    'supplierReference': 'ABC-123',
    'refreshFrequency': 'HOURLY',
})


def test_suppliers_list(client: OctoClient, mocked_responses):
    client.get_suppliers()
    assert client.suppliers == [
        m.Supplier(
            id='0001',
            name='Acme Tour Co.',
            endpoint='https://api.my-booking-platform.com/v1',
            contact=m.SupplierContact(
                address='123 Main St, Anytown USA',
                email='info@acme-tours.co.fake',
                telephone='+1 888-555-1212',
                description=None,
                website='https://acme-tours.co.fake',
                extra_fields={
                    'country': 'US',
                },
            ),
            extra_fields={
                'timezone': 'EST',
            },
        )
    ]
    assert client.supplier_url_map == {
        '0001': 'https://api.my-booking-platform.com/v1',
    }
    assert len(mocked_responses.calls) == 1, 'Too many requests'
    assert mocked_responses.calls[0].request.url == 'http://fake-api.local/suppliers'
    assert mocked_responses.calls[0].request.headers['Authorization'] == 'Bearer bar'


def test_products(client: OctoClient, mocked_responses):
    mocked_responses.add(responses.GET, 'https://api.my-booking-platform.com/v1/suppliers/0001/products', json=[
        {
            'id': 'a491687f-1dce-4be2-bc47-0157541bc8c1',
            'internalName': 'Studio Tour',
            'reference': 'STUDIO',
            'locale': 'en',
            'timeZone': 'America/Los_Angeles',
            'instantConfirmation': True,
            'instantDelivery': True,
            'availabilityType': 'START_TIME',
            'deliveryFormats': ['PDF_URL', 'QRCODE'],
            'deliveryMethods': ['TICKET', 'VOUCHER'],
            'redemptionMethod': 'DIGITAL',
            'capabilities': [],
            'options': [
                {
                    'id': '345314bb-aaaf-4ba2-b3ef-ff15ea39a0ae',
                    'internalName': 'Studio Tour',
                    'reference': None,
                    'units': [
                        {
                            'id': 'adult',
                            'internalName': 'Studio Tour',
                            'reference': None,
                            'type': 'ADULT',
                        }
                    ]
                }
            ]
        }, {
            'id': '3e803053-6f39-46f7-8a67-2114de59b135',
            'internalName': 'VIP Tour',
            'reference': 'VIP',
            'locale': 'en',
            'timeZone': 'America/Los_Angeles',
            'instantConfirmation': True,
            'instantDelivery': True,
            'availabilityType': 'START_TIME',
            'deliveryFormats': ['PDF_URL', 'QRCODE'],
            'deliveryMethods': ['TICKET', 'VOUCHER'],
            'redemptionMethod': 'DIGITAL',
            'capabilities': [],
            'options': [
                {
                    'id': 'DEFAULT',
                    'internalName': 'DEFAULT',
                    'reference': None,
                    'units': [
                        {
                            'id': 'adult',
                            'internalName': 'VIP Tour',
                            'reference': None,
                            'type': 'ADULT',
                        }
                    ]
                }
            ]
        }
    ])
    products = client.get_products(supplier_id='0001')
    assert products == [
        m.Product(
            id='a491687f-1dce-4be2-bc47-0157541bc8c1',
            internalName='Studio Tour',
            reference='STUDIO',
            locale='en',
            timeZone='America/Los_Angeles',
            instantConfirmation=True,
            instantDelivery=True,
            availabilityType='START_TIME',
            deliveryFormats=['PDF_URL', 'QRCODE'],
            deliveryMethods=['TICKET', 'VOUCHER'],
            redemptionMethod='DIGITAL',
            capabilities=[],
            options=[
                m.Option(
                    id='345314bb-aaaf-4ba2-b3ef-ff15ea39a0ae',
                    internalName='Studio Tour',
                    units=[
                        m.Unit(
                            id='adult',
                            internalName='Studio Tour',
                            type='ADULT',
                            reference=None,
                            extra_fields={},
                        )
                    ],
                    reference=None,
                    extra_fields={},
                )
            ],
            extra_fields={},
        ),
        m.Product(
            id='3e803053-6f39-46f7-8a67-2114de59b135',
            internalName='VIP Tour',
            reference='VIP',
            locale='en',
            timeZone='America/Los_Angeles',
            instantConfirmation=True,
            instantDelivery=True,
            availabilityType='START_TIME',
            deliveryFormats=['PDF_URL', 'QRCODE'],
            deliveryMethods=['TICKET', 'VOUCHER'],
            redemptionMethod='DIGITAL',
            capabilities=[],
            options=[
                m.Option(
                    id='DEFAULT',
                    internalName='DEFAULT',
                    units=[
                        m.Unit(
                            id='adult',
                            internalName='VIP Tour',
                            type='ADULT',
                            reference=None,
                            extra_fields={},
                        )
                    ],
                    reference=None,
                    extra_fields={},
                )
            ],
            extra_fields={},
        ),
    ]
    assert len(mocked_responses.calls) == 2, 'Too many requests'
    assert mocked_responses.calls[1].request.url == (
        'https://api.my-booking-platform.com/v1/suppliers/0001/products'
    )


def test_calendar(client: OctoClient, mocked_responses):
    mocked_responses.add(
        responses.GET,
        'https://api.my-booking-platform.com/v1/suppliers/0001/availability/calendar',
        json=[
            {
                "localDate": "2020-06-01",
                "status": "AVAILABLE",
                "vacancies": 14,
            },
            {
                "localDate": "2020-06-01",
                "status": "AVAILABLE",
                "vacancies": 18,
            },
            {
                "localDate": "2020-06-02",
                "status": "AVAILABLE",
                "vacancies": 28,
            },
            {
                "localDate": "2020-06-02",
                "status": "AVAILABLE",
                "vacancies": 31,
            }
        ]
    )
    availability = client.get_calendar(
        supplier_id='0001',
        product_id='foo',
        option_id='bar',
        start_date=date(2020, 6, 1),
        end_date=date(2020, 6, 2),
    )
    assert availability == [
        m.AvailabilityCalendarItem(
            localDate=date(2020, 6, 1),
            status='AVAILABLE',
            vacancies=14,
            extra_fields={},
        ),
        m.AvailabilityCalendarItem(
            localDate=date(2020, 6, 1),
            status='AVAILABLE',
            vacancies=18,
            extra_fields={},
        ),
        m.AvailabilityCalendarItem(
            localDate=date(2020, 6, 2),
            status='AVAILABLE',
            vacancies=28,
            extra_fields={},
        ),
        m.AvailabilityCalendarItem(
            localDate=date(2020, 6, 2),
            status='AVAILABLE',
            vacancies=31,
            extra_fields={},
        ),
    ]
    assert len(mocked_responses.calls) == 2, 'Too many requests'
    assert mocked_responses.calls[1].request.url == (
        'https://api.my-booking-platform.com/v1/suppliers/0001/availability/calendar'
        '?productId=foo'
        '&optionId=bar'
        '&localDateStart=2020-06-01'
        '&localDateEnd=2020-06-02'
    )


def test_availability(client: OctoClient, mocked_responses):
    mocked_responses.add(responses.GET, 'https://api.my-booking-platform.com/v1/suppliers/0001/availability', json=[
        {
            'id': '2020-12-01T09:00:00-08:00',
            'localDateTimeStart': '2020-12-01T09:00:00-08:00',
            'localDateTimeEnd': '2020-12-01T11:00:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 14,
        },
        {
            'id': '2020-12-01T09:30:00-08:00',
            'localDateTimeStart': '2020-12-01T09:30:00-08:00',
            'localDateTimeEnd': '2020-12-01T11:30:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 13,
        },
        {
            'id': '2020-12-01T10:00:00-08:00',
            'localDateTimeStart': '2020-12-01T10:00:00-08:00',
            'localDateTimeEnd': '2020-12-01T12:00:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 12,
        },
    ])
    availability = client.get_availability(
        supplier_id='0001',
        product_id='bar',
        option_id='baz',
        start_date=date(2020, 12, 1),
        end_date=date(2020, 12, 2),
    )
    assert availability == [
        m.AvailabilityItem(
            id='2020-12-01T09:00:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 9, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 11, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=14,
            extra_fields={},
        ),
        m.AvailabilityItem(
            id='2020-12-01T09:30:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 9, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 11, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=13,
            extra_fields={},
        ),
        m.AvailabilityItem(
            id='2020-12-01T10:00:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 10, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 12, 0, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=12,
            extra_fields={},
        ),
    ]
    assert len(mocked_responses.calls) == 2, 'Too many requests'
    assert mocked_responses.calls[1].request.url == (
        'https://api.my-booking-platform.com/v1/suppliers/0001/availability'
        '?productId=bar'
        '&optionId=baz'
        '&localDateStart=2020-12-01'
        '&localDateEnd=2020-12-02'
    )


def test_test_availability(client: OctoClient, mocked_responses):
    mocked_responses.add(responses.POST, 'https://api.my-booking-platform.com/v1/suppliers/0001/availability', json=[
        {
            'id': '2020-12-01T15:30:00-08:00',
            'localDateTimeStart': '2020-12-01T15:30:00-08:00',
            'localDateTimeEnd': '2020-12-01T17:30:00-08:00',
            'status': 'AVAILABLE',
            'vacancies': 14,
        }
    ])
    availability = client.test_availability(
        supplier_id='0001',
        product_id='bar',
        option_id='baz',
        availability_ids=['2020-12-01T15:30:00-08:00'],
        units=[m.UnitQuantity(unitId='adult', quantity=2, extra_fields={})],
    )
    assert availability == [
        m.AvailabilityItem(
            id='2020-12-01T15:30:00-08:00',
            localDateTimeStart=datetime(2020, 12, 1, 15, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            localDateTimeEnd=datetime(2020, 12, 1, 17, 30, tzinfo=timezone(timedelta(days=-1, seconds=57600))),
            status='AVAILABLE',
            vacancies=14,
            extra_fields={},
        )
    ]
    assert len(mocked_responses.calls) == 2, 'Too many requests'
    assert mocked_responses.calls[1].request.url == 'https://api.my-booking-platform.com/v1/suppliers/0001/availability'
    request_json = json.loads(mocked_responses.calls[1].request.body)
    assert request_json == {
        'productId': 'bar',
        'optionId': 'baz',
        'availabilityIds': ['2020-12-01T15:30:00-08:00'],
        'units': [{
            'unitId': 'adult',
            'quantity': 2
        }]
    }


def test_create_booking(client: OctoClient, mocked_responses):
    mocked_responses.add(
        responses.POST,
        'https://api.my-booking-platform.com/v1/suppliers/0001/bookings',
        json=BOOKING_JSON
    )
    booking = client.create_booking(
        supplier_id='0001',
        booking_request=m.BookingRequest(
            uuid='f149068e-300e-452a-a856-3f091239f1d7',
            productId='adult',
            optionId='LR1-01',
            availabilityId='28271273-a317-40fc-8f42-79725a7072a3',
            unitItems=[
                m.UnitItem(
                    uuid='6be0409f-181e-4520-acc1-cc6791896859',
                    unitId='adult',
                    extra_fields={},
                )
            ],
            extra_fields={},
        ),
    )
    assert booking == BOOKING_MODEL
    assert len(mocked_responses.calls) == 2, 'Too many requests'
    assert mocked_responses.calls[1].request.url == 'https://api.my-booking-platform.com/v1/suppliers/0001/bookings'
    request_json = json.loads(mocked_responses.calls[1].request.body)
    assert request_json == {
        'uuid': 'f149068e-300e-452a-a856-3f091239f1d7',
        'productId': 'adult',
        'optionId': 'LR1-01',
        'availabilityId': '28271273-a317-40fc-8f42-79725a7072a3',
        'unitItems': [{
            'uuid': '6be0409f-181e-4520-acc1-cc6791896859',
            'unitId': 'adult',
            'resellerReference': None,
            'extra_fields': {},
        }],
        'holdExpirationMinutes': None,
        'resellerReference': None,
    }


def test_booking_confirmation(client: OctoClient, mocked_responses):
    mocked_responses.add(
        responses.POST,
        'https://api.my-booking-platform.com/v1/suppliers/0001/bookings/7df49d62-57ad-44be-8373-e4c2fe7e63fe/confirm',
        json=BOOKING_JSON,
    )
    booking = client.confirm_booking(
        supplier_id='0001',
        uuid='7df49d62-57ad-44be-8373-e4c2fe7e63fe',
        confirmation_request=m.BookingConfirmationRequest(
            resellerReference='001-002',
            contact=m.Contact(
                fullName='Mr. Traveller',
                emailAddress='traveller@fake.local',
                phoneNumber='+1 555-555-1212',
                locales=['en-GB', 'en-US', 'en'],
                country='GB',
                extra_fields={},
            ),
            extra_fields={},
        )
    )
    assert booking == BOOKING_MODEL
    assert len(mocked_responses.calls) == 2, 'Too many requests'
    assert mocked_responses.calls[1].request.url == (
        'https://api.my-booking-platform.com/v1/suppliers/0001/bookings/7df49d62-57ad-44be-8373-e4c2fe7e63fe/confirm'
    )
    request_json = json.loads(mocked_responses.calls[1].request.body)
    assert request_json == {
        'contact': {
            'fullName': 'Mr. Traveller',
            'emailAddress': 'traveller@fake.local',
            'phoneNumber': '+1 555-555-1212',
            'locales': ['en-GB', 'en-US', 'en'],
            'country': 'GB',
            'extra_fields': {},
        },
        'resellerReference': '001-002'
    }


def test_booking_details(client: OctoClient, mocked_responses):
    mocked_responses.add(
        responses.GET,
        'https://api.my-booking-platform.com/v1/suppliers/0001/bookings/7df49d62-57ad-44be-8373-e4c2fe7e63fe',
        json=BOOKING_JSON,
    )
    booking = client.get_booking_details(
        supplier_id='0001',
        uuid='7df49d62-57ad-44be-8373-e4c2fe7e63fe'
    )
    assert booking == BOOKING_MODEL
    assert len(mocked_responses.calls) == 2, 'Too many requests'
    assert mocked_responses.calls[1].request.url == (
        'https://api.my-booking-platform.com/v1/suppliers/0001/bookings/7df49d62-57ad-44be-8373-e4c2fe7e63fe'
    )
