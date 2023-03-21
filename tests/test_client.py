from datetime import date, datetime, time, timedelta, timezone

import responses

from octo_client import OctoClient, const
from octo_client import models as m

from .conftest import load_json_response


def test_get_suppliers(client: OctoClient, mocked_responses):
    # WHEN
    suppliers = client.get_suppliers()

    # THEN
    assert suppliers == [
        m.Supplier(
            id="48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
            name="John Doe's company",
            endpoint="http://fake-api.local",
            contact=m.SupplierContact(
                website=None, email="john.doe@email.com", telephone=None, address=None
            ),
        )
    ]
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 1, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert mocked_responses.calls[0].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[0].request.body is None


def test_get_supplier(client: OctoClient, mocked_responses):
    # GIVEN
    supplier_response = load_json_response("supplier.json")
    mocked_responses.add(
        responses.GET,
        "http://fake-api.local/suppliers/48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
        json=supplier_response,
    )

    # WHEN
    response = client.get_supplier("48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2")

    # THEN
    assert response == m.Supplier(
        id="48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
        name="John Doe's company",
        endpoint="http://fake-api.local",
        contact=m.SupplierContact(
            website=None, email="john.doe@email.com", telephone=None, address=None
        ),
    )
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert (
        mocked_responses.calls[1].request.url
        == "http://fake-api.local/suppliers/48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2"
    )
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body is None


def test_get_products(client: OctoClient, mocked_responses):
    # GIVEN
    products_response = load_json_response("products.json")
    mocked_responses.add(responses.GET, "http://fake-api.local/products", json=products_response)

    # WHEN
    response = client.get_products("48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2")

    # THEN
    assert response == [
        m.Product(
            id="6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
            internalName="Amazon River Tour",
            locale="en-GB",
            timeZone="Europe/London",
            allowFreesale=True,
            instantConfirmation=True,
            instantDelivery=True,
            availabilityRequired=True,
            availabilityType=const.AvailabilityType.START_TIME,
            redemptionMethod=const.RedemptionMethod.DIGITAL,
            options=[
                m.Option(
                    id="DEFAULT",
                    default=True,
                    internalName="Private Morning Tour",
                    cancellationCutoff="1 hour",
                    cancellationCutoffAmount=1,
                    cancellationCutoffUnit=const.CancellationCutoffUnit.hour,
                    restrictions=m.OptionRestriction(minUnits=None, maxUnits=10),
                    reference="VIP-MORN",
                    availabilityLocalStartTimes=["09:00"],
                    requiredContactFields=[const.RequiredContactField.firstName],
                    units=[
                        m.Unit(
                            id="adult_697e3ce8-1860-4cbf-80ad-95857df1f640",
                            internalName="Adult(s)",
                            type=const.UnitType.YOUTH,
                            restrictions=m.UnitRestrictions(
                                minAge=3,
                                maxAge=17,
                                idRequired=True,
                                paxCount=1,
                                accompaniedBy=["adult_697e3ce8-1860-4cbf-80ad-95857df1f640"],
                                minQuantity=2,
                                maxQuantity=7,
                            ),
                            requiredContactFields=[const.RequiredContactField.firstName],
                            reference="LR1-01-new",
                        )
                    ],
                )
            ],
            deliveryFormats=[const.DeliveryFormat.QRCODE],
            deliveryMethods=[const.DeliveryMethod.VOUCHER],
            reference="AMZN",
        )
    ]
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert mocked_responses.calls[1].request.url == "http://fake-api.local/products"
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body is None


def test_get_product(client: OctoClient, mocked_responses):
    # GIVEN
    products_response = load_json_response("product.json")
    mocked_responses.add(
        responses.GET,
        "http://fake-api.local/products/6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
        json=products_response,
    )

    # WHEN
    response = client.get_product(
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2", "6b903d44-dc24-4ca4-ae71-6bde6c4f4854"
    )

    # THEN
    assert response == m.Product(
        id="6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
        internalName="Amazon River Tour",
        locale="en-GB",
        timeZone="Europe/London",
        allowFreesale=True,
        instantConfirmation=True,
        instantDelivery=True,
        availabilityRequired=True,
        availabilityType=const.AvailabilityType.START_TIME,
        redemptionMethod=const.RedemptionMethod.DIGITAL,
        options=[
            m.Option(
                id="DEFAULT",
                default=True,
                internalName="Private Morning Tour",
                cancellationCutoff="1 hour",
                cancellationCutoffAmount=1,
                cancellationCutoffUnit=const.CancellationCutoffUnit.hour,
                restrictions=m.OptionRestriction(minUnits=None, maxUnits=10),
                reference="VIP-MORN",
                availabilityLocalStartTimes=["09:00"],
                requiredContactFields=[const.RequiredContactField.firstName],
                units=[
                    m.Unit(
                        id="adult_697e3ce8-1860-4cbf-80ad-95857df1f640",
                        internalName="Adult(s)",
                        type=const.UnitType.YOUTH,
                        restrictions=m.UnitRestrictions(
                            minAge=3,
                            maxAge=17,
                            idRequired=True,
                            paxCount=1,
                            accompaniedBy=["adult_697e3ce8-1860-4cbf-80ad-95857df1f640"],
                            minQuantity=2,
                            maxQuantity=7,
                        ),
                        requiredContactFields=[const.RequiredContactField.firstName],
                        reference="LR1-01-new",
                    )
                ],
            )
        ],
        deliveryFormats=[const.DeliveryFormat.QRCODE],
        deliveryMethods=[const.DeliveryMethod.VOUCHER],
        reference="AMZN",
    )
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert (
        mocked_responses.calls[1].request.url
        == "http://fake-api.local/products/6b903d44-dc24-4ca4-ae71-6bde6c4f4854"
    )
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body is None


def test_availability_opening_hours(client: OctoClient, mocked_responses):
    # GIVEN
    availability_response = load_json_response("availability_opening_hours.json")
    mocked_responses.add(
        responses.POST, "http://fake-api.local/availability", json=availability_response
    )

    # WHEN
    response = client.availability_check(
        supplier_id="48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
        product_id="6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
        option_id="DEFAULT",
        local_date_start=date(2022, 6, 25),
        local_date_end=date(2022, 6, 30),
    )

    # THEN
    assert response == [
        m.Availability(
            id="2022-06-30T00:00:00+01:00",
            localDateTimeStart=datetime(
                2022, 6, 30, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
            ),
            localDateTimeEnd=datetime(2022, 7, 1, 0, 0, tzinfo=timezone(timedelta(seconds=3600))),
            allDay=True,
            available=True,
            status=const.AvailabilityStatus.FREESALE,
            utcCutoffAt=datetime(2022, 6, 29, 22, 0, tzinfo=timezone.utc),
            openingHours=[m.OpeningHours(from_=time(9, 0), to=time(17, 0))],
            vacancies=None,
            capacity=None,
            maxUnits=None,
        )
    ]
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert mocked_responses.calls[1].request.url == "http://fake-api.local/availability"
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body


def test_availability_start_times(client: OctoClient, mocked_responses):
    # GIVEN
    availability_response = load_json_response("availability_start_times.json")
    mocked_responses.add(
        responses.POST, "http://fake-api.local/availability", json=availability_response
    )

    # WHEN
    response = client.availability_check(
        supplier_id="48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
        product_id="6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
        option_id="DEFAULT",
        local_date_start=date(2022, 6, 25),
        local_date_end=date(2022, 6, 30),
    )

    # THEN
    assert response == [
        m.Availability(
            id="2022-06-30T12:00:00+01:00",
            localDateTimeStart=datetime(
                2022, 6, 30, 12, 0, tzinfo=timezone(timedelta(seconds=3600))
            ),
            localDateTimeEnd=datetime(2022, 6, 30, 14, 0, tzinfo=timezone(timedelta(seconds=3600))),
            allDay=False,
            available=True,
            status=const.AvailabilityStatus.AVAILABLE,
            utcCutoffAt=datetime(2022, 6, 30, 10, 0, tzinfo=timezone.utc),
            openingHours=[],
            vacancies=10,
            capacity=10,
            maxUnits=None,
        ),
        m.Availability(
            id="2022-06-30T14:00:00+01:00",
            localDateTimeStart=datetime(
                2022, 6, 30, 14, 0, tzinfo=timezone(timedelta(seconds=3600))
            ),
            localDateTimeEnd=datetime(2022, 6, 30, 16, 0, tzinfo=timezone(timedelta(seconds=3600))),
            allDay=False,
            available=True,
            status=const.AvailabilityStatus.AVAILABLE,
            utcCutoffAt=datetime(2022, 6, 30, 12, 0, tzinfo=timezone.utc),
            openingHours=[],
            vacancies=10,
            capacity=10,
            maxUnits=None,
        ),
    ]
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert mocked_responses.calls[1].request.url == "http://fake-api.local/availability"
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body


def test_calendar_opening_hours(client: OctoClient, mocked_responses):
    # GIVEN
    availability_response = load_json_response("calendar_opening_hours.json")
    mocked_responses.add(
        responses.POST, "http://fake-api.local/availability/calendar", json=availability_response
    )

    # WHEN
    response = client.get_calendar(
        supplier_id="48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
        product_id="6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
        option_id="DEFAULT",
        local_date_start=date(2022, 6, 10),
        local_date_end=date(2022, 6, 20),
    )

    # THEN
    assert response == [
        m.AvailabilityCalendarItem(
            localDate=date(2022, 6, 14),
            available=True,
            status=const.AvailabilityStatus.FREESALE,
            vacancies=None,
            capacity=None,
            openingHours=[m.OpeningHours(from_=time(9, 0), to=time(17, 0))],
        ),
        m.AvailabilityCalendarItem(
            localDate=date(2022, 6, 15),
            available=True,
            status=const.AvailabilityStatus.FREESALE,
            vacancies=None,
            capacity=None,
            openingHours=[m.OpeningHours(from_=time(9, 0), to=time(17, 0))],
        ),
        m.AvailabilityCalendarItem(
            localDate=date(2022, 6, 16),
            available=True,
            status=const.AvailabilityStatus.FREESALE,
            vacancies=None,
            capacity=None,
            openingHours=[m.OpeningHours(from_=time(9, 0), to=time(17, 0))],
        ),
    ]
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert mocked_responses.calls[1].request.url == "http://fake-api.local/availability/calendar"
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body


def test_calendar_start_times(client: OctoClient, mocked_responses):
    # GIVEN
    availability_response = load_json_response("calendar_start_times.json")
    mocked_responses.add(
        responses.POST, "http://fake-api.local/availability/calendar", json=availability_response
    )

    # WHEN
    response = client.get_calendar(
        supplier_id="48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
        product_id="6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
        option_id="DEFAULT",
        local_date_start=date(2022, 6, 10),
        local_date_end=date(2022, 6, 20),
    )

    # THEN
    assert response == [
        m.AvailabilityCalendarItem(
            localDate=date(2022, 6, 14),
            available=True,
            status=const.AvailabilityStatus.AVAILABLE,
            vacancies=20,
            capacity=20,
            openingHours=[],
        ),
        m.AvailabilityCalendarItem(
            localDate=date(2022, 6, 15),
            available=True,
            status=const.AvailabilityStatus.AVAILABLE,
            vacancies=10,
            capacity=10,
            openingHours=[],
        ),
        m.AvailabilityCalendarItem(
            localDate=date(2022, 6, 16),
            available=True,
            status=const.AvailabilityStatus.AVAILABLE,
            vacancies=10,
            capacity=10,
            openingHours=[],
        ),
    ]
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert mocked_responses.calls[1].request.url == "http://fake-api.local/availability/calendar"
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body


def test_reservation(client: OctoClient, mocked_responses):
    # GIVEN
    reservation_response = load_json_response("reservation.json")
    mocked_responses.add(
        responses.POST, "http://fake-api.local/bookings", json=reservation_response
    )

    # WHEN
    response = client.booking_reservation(
        supplier_id="48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2",
        uuid="559aed3d-6d5b-4fe0-bfca-99f5e7218a56",
        product_id="6b903d44-dc24-4ca4-ae71-6bde6c4f4854",
        option_id="DEFAULT",
        availability_id="2021-10-27T00:00:00-04:00",
        unit_items=[
            m.UnitItem(
                uuid="3b1bc2ee-3155-4738-9471-f49842a07327",
                unitId="youth_f6446706-885a-437c-8461-efd6d7080910",
            )
        ],
    )

    # THEN
    assert response == m.Booking(
        id="602a9fdf-5c79-4984-9474-7e14da9b6027",
        uuid="a88b4b8d-9c3b-4a09-ba27-323b43af57e4",
        testMode=True,
        status=const.BookingStatus.ON_HOLD,
        productId="1",
        product=m.Product(
            id="1",
            internalName="PPU | OH",
            locale="en",
            timeZone="Europe/London",
            allowFreesale=False,
            instantConfirmation=True,
            instantDelivery=True,
            availabilityRequired=True,
            availabilityType=const.AvailabilityType.OPENING_HOURS,
            redemptionMethod=const.RedemptionMethod.DIGITAL,
            options=[
                m.Option(
                    id="DEFAULT",
                    default=True,
                    internalName="DEFAULT",
                    cancellationCutoff="0 hours",
                    cancellationCutoffAmount=0,
                    cancellationCutoffUnit=const.CancellationCutoffUnit.hour,
                    restrictions=m.OptionRestriction(
                        minUnits=0,
                        maxUnits=None,
                    ),
                    reference=None,
                    availabilityLocalStartTimes=["00:00"],
                    requiredContactFields=[],
                    units=[
                        m.Unit(
                            id="adult",
                            internalName="adult",
                            type=const.UnitType.ADULT,
                            restrictions=m.UnitRestrictions(
                                minAge=18,
                                maxAge=100,
                                idRequired=False,
                                paxCount=1,
                                accompaniedBy=[],
                                minQuantity=None,
                                maxQuantity=None,
                            ),
                            requiredContactFields=[],
                            reference="adult",
                        )
                    ],
                )
            ],
            deliveryFormats=[
                const.DeliveryFormat.PDF_URL,
                const.DeliveryFormat.QRCODE,
            ],
            deliveryMethods=[
                const.DeliveryMethod.TICKET,
                const.DeliveryMethod.VOUCHER,
            ],
            reference=None,
        ),
        optionId="DEFAULT",
        option=m.Option(
            id="DEFAULT",
            default=True,
            internalName="DEFAULT",
            cancellationCutoff="0 hours",
            cancellationCutoffAmount=0,
            cancellationCutoffUnit=const.CancellationCutoffUnit.hour,
            restrictions=m.OptionRestriction(
                minUnits=0,
                maxUnits=None,
            ),
            reference=None,
            availabilityLocalStartTimes=["00:00"],
            requiredContactFields=[],
            units=[
                m.Unit(
                    id="adult",
                    internalName="adult",
                    type=const.UnitType.ADULT,
                    restrictions=m.UnitRestrictions(
                        minAge=18,
                        maxAge=100,
                        idRequired=False,
                        paxCount=1,
                        accompaniedBy=[],
                        minQuantity=None,
                        maxQuantity=None,
                    ),
                    requiredContactFields=[],
                    reference="adult",
                )
            ],
        ),
        cancellable=True,
        freesale=False,
        availabilityId="2022-04-30T00:00:00+01:00",
        availability=m.BookingAvailability(
            id="2022-04-30T00:00:00+01:00",
            localDateTimeStart=datetime(
                2022, 4, 30, 0, 0, tzinfo=timezone(timedelta(seconds=3600))
            ),
            localDateTimeEnd=datetime(2022, 5, 1, 0, 0, tzinfo=timezone(timedelta(seconds=3600))),
            allDay=True,
            openingHours=[m.OpeningHours(from_=time(9, 0), to=time(17, 0))],
        ),
        contact=m.BookingContact(
            locales=[],
            fullName=None,
            firstName=None,
            lastName=None,
            emailAddress=None,
            phoneNumber=None,
            postalCode=None,
            country=None,
            notes=None,
        ),
        notes=None,
        voucher=m.Ticket(
            redemptionMethod=const.RedemptionMethod.DIGITAL, utcRedeemedAt=None, deliveryOptions=[]
        ),
        resellerReference=None,
        supplierReference="XOPSUT",
        utcCreatedAt=datetime(2022, 5, 25, 10, 34, 22, tzinfo=timezone.utc),
        utcUpdatedAt=datetime(2022, 5, 25, 10, 34, 22, tzinfo=timezone.utc),
        utcExpiresAt=datetime(2022, 5, 25, 11, 4, 22, tzinfo=timezone.utc),
        utcRedeemedAt=None,
        utcConfirmedAt=None,
        cancellation=None,
        deliveryMethods=[
            const.DeliveryMethod.TICKET,
            const.DeliveryMethod.VOUCHER,
        ],
        unitItems=[
            m.BookingUnitItem(
                uuid="6cbd2582-1345-4d8d-8223-ad004beebc1a",
                unitId="adult",
                unit=m.Unit(
                    id="adult",
                    internalName="adult",
                    type=const.UnitType.ADULT,
                    restrictions=m.UnitRestrictions(
                        minAge=18,
                        maxAge=100,
                        idRequired=False,
                        paxCount=1,
                        accompaniedBy=[],
                        minQuantity=None,
                        maxQuantity=None,
                    ),
                    requiredContactFields=[],
                    reference="adult",
                ),
                status=const.BookingStatus.ON_HOLD,
                contact=m.BookingContact(
                    locales=[],
                    fullName=None,
                    firstName=None,
                    lastName=None,
                    emailAddress=None,
                    phoneNumber=None,
                    postalCode=None,
                    country=None,
                    notes=None,
                ),
                resellerReference=None,
                supplierReference="CBIYWQ",
                utcRedeemedAt=None,
                ticket=m.Ticket(
                    redemptionMethod=const.RedemptionMethod.DIGITAL,
                    utcRedeemedAt=None,
                    deliveryOptions=[],
                ),
            )
        ],
    )
    assert client.supplier_url_map == {
        "48b4d2e9-cd8b-4ac2-a5ee-4217bf2622d2": "http://fake-api.local",
    }
    assert len(mocked_responses.calls) == 2, "Too many requests"
    assert mocked_responses.calls[0].request.url == "http://fake-api.local/suppliers"
    assert mocked_responses.calls[1].request.url == "http://fake-api.local/bookings"
    assert mocked_responses.calls[1].request.headers["Authorization"] == "Bearer secret-token"
    assert mocked_responses.calls[1].request.body
