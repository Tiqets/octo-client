from typing import List

import pytest

from octo_client.const import DeliveryFormat
from octo_client.const import UnitType
from octo_client.models import DeliveryOption
from octo_client.models import Product
from octo_client.models import Unit


@pytest.mark.parametrize(
    "input_unity_type_value, expected_value", [
        ("CHILDREN", UnitType.OTHER),
        (UnitType.OTHER.value, UnitType.OTHER),
        (UnitType.ADULT.value, UnitType.ADULT),
        (UnitType.YOUTH.value, UnitType.YOUTH),
        (UnitType.CHILD.value, UnitType.CHILD),
        (UnitType.INFANT.value, UnitType.INFANT),
        (UnitType.FAMILY.value, UnitType.FAMILY),
        (UnitType.SENIOR.value, UnitType.SENIOR),
        (UnitType.STUDENT.value, UnitType.STUDENT),
        (UnitType.MILITARY.value, UnitType.MILITARY),
    ]
)
def test_map_unknown_unit_type(input_unity_type_value: str, expected_value: UnitType):
    # GIVEN
    data = {
        "id": "12345",
        "internalName": "test name",
        "type": input_unity_type_value,
        "restrictions": {
            "minAge": 1,
            "maxAge": 2,
            "idRequired": True,
            "paxCount": 3,
            "accompaniedBy": [],
        },
        "requiredContactFields": [],
        "reference": "1a2b3c",
    }

    # WHEN
    instance = Unit.from_dict(data)

    # THEN
    assert instance.type == expected_value


@pytest.mark.parametrize(
    "input_delivery_format_value, expected_value", [
        ("PKPASS_URL", DeliveryFormat.OTHER),
        (DeliveryFormat.CODE128.value, DeliveryFormat.CODE128),
        (DeliveryFormat.QRCODE.value, DeliveryFormat.QRCODE),
        (DeliveryFormat.PDF_URL.value, DeliveryFormat.PDF_URL),
    ]
)
def test_map_unknown_delivery_format(input_delivery_format_value: str, expected_value: DeliveryFormat):
    # GIVEN
    data = {
        "deliveryFormat": input_delivery_format_value,
        "deliveryValue": "test value",
    }

    # WHEN
    instance = DeliveryOption.from_dict(data)

    # THEN
    assert instance.deliveryFormat == expected_value


@pytest.mark.parametrize(
    "input_delivery_format_value, expected_value", [
        (["PKPASS_URL"], [DeliveryFormat.OTHER]),
        ([DeliveryFormat.CODE128.value], [DeliveryFormat.CODE128]),
    ]
)
def test_map_unknown_delivery_format_in_product(input_delivery_format_value: str, expected_value: List[DeliveryFormat]):
    # GIVEN
    data = {
        "deliveryFormats": input_delivery_format_value,
        "id": "12345",
        "internalName": "1a2b3c",
        "locale": "en-US",
        "timeZone": "UTC",
        "allowFreesale": True,
        "instantConfirmation": True,
        "instantDelivery": True,
        "availabilityRequired": True,
        "availabilityType": "START_TIME",
        "redemptionMethod": "DIGITAL",
        "options": [],
        "deliveryMethods": [],
    }

    # WHEN
    instance = Product.from_dict(data)

    # THEN
    assert instance.deliveryFormats == expected_value
