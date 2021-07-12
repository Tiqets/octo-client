from dataclasses import asdict, dataclass, field, fields
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

import attr
from tonalite import Config, from_dict


@dataclass
@attr.s(auto_attribs=True)
class BaseModel:

    # extra_fields: Optional[dict] = field(default_factory=dict)
    # ^ this field cannot be inherited by other models due to a python bug
    # with ordering fields that have any default value and the ones that do not
    # "error: Attributes without a default cannot follow attributes with one"
    # https://bugs.python.org/issue36077
    # Workaround: adding this field at the end of every model

    @staticmethod
    def _datetime_from_iso_format(datetime_str: Optional[str]) -> Optional[datetime]:
        if datetime_str:
            return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return None

    def as_dict(self) -> dict:
        """
        Dumps dataclass into dictionary.
        """
        model_as_dict = asdict(self)
        model_as_dict.update(model_as_dict.pop('extra_fields'))
        return model_as_dict

    @classmethod
    def from_dict(cls, data: dict, config=None):
        """
        Populating data class from a dictionary with strict type checking.
        """
        if config is None:
            config = Config(strict=True, type_hooks={
                date: date.fromisoformat,
                datetime: cls._datetime_from_iso_format,
            })

        extra_fields = set(data.keys()).difference([f.name for f in fields(cls)])
        data['extra_fields'] = {}
        for extra_field in extra_fields:
            data['extra_fields'][extra_field] = data.pop(extra_field)
        return from_dict(cls, data=data, config=config)


@dataclass
class SupplierContact(BaseModel):
    email: str
    address: Optional[str] = None
    telephone: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Supplier(BaseModel):
    id: str
    name: str
    endpoint: str
    contact: SupplierContact
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Capability(BaseModel):
    id: str
    revision: int
    required: bool
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Unit(BaseModel):
    id: str
    internalName: str
    type: str
    reference: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Option(BaseModel):
    id: str
    internalName: str
    units: List[Unit]
    reference: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Product(BaseModel):
    id: str
    internalName: str
    locale: str
    timeZone: str
    instantConfirmation: bool
    instantDelivery: bool
    availabilityType: str
    deliveryFormats: List[str]
    deliveryMethods: List[str]
    redemptionMethod: str
    options: List[Option]
    capabilities: List[Capability] = field(default_factory=list)
    reference: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class AvailabilityCalendarItem(BaseModel):
    localDate: date
    status: str
    vacancies: Optional[int] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class AvailabilityItem(BaseModel):
    id: str
    localDateTimeStart: datetime
    localDateTimeEnd: datetime
    status: str
    vacancies: Optional[int] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class UnitItem(BaseModel):
    uuid: str
    unitId: str
    resellerReference: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class UnitQuantity(BaseModel):
    unitId: str
    quantity: int
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class BookingRequest(BaseModel):
    uuid: str
    productId: str
    optionId: str
    availabilityId: str
    unitItems: List[UnitItem]
    holdExpirationMinutes: Optional[int] = None
    resellerReference: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Availability(BaseModel):
    id: str
    localDateTimeStart: datetime
    localDateTimeEnd: datetime
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Contact(BaseModel):
    locales: List[str]
    fullName: Optional[str] = None
    emailAddress: Optional[str] = None
    phoneNumber: Optional[str] = None
    country: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class DeliveryOption(BaseModel):
    deliveryFormat: str
    deliveryValue: str
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Ticket(BaseModel):
    deliveryOptions: List[DeliveryOption]
    redemptionMethod: str
    utcDeliveredAt: Optional[datetime] = None
    utcRedeemedAt: Optional[datetime] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class BookingTicket(BaseModel):
    deliveryOptions: List[DeliveryOption]
    redemptionMethod: str
    utcDeliveredAt: Optional[datetime] = None
    utcRedeemedAt: Optional[datetime] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class UnitItemTicket(BaseModel):
    uuid: str
    unitId: str
    ticket: Optional[BookingTicket] = None
    resellerReference: Optional[str] = None
    supplierReference: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class CancellationRequest(BaseModel):
    reason: str
    reasonDetails: str
    status: str
    refund: str
    utcRequestedAt: datetime
    utcHoldExpiration: Optional[datetime] = None
    utcConfirmedAt: Optional[datetime] = None
    utcResolvedAt: Optional[datetime] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class Booking(BaseModel):
    uuid: str
    status: str
    productId: str
    optionId: str
    availability: Availability
    deliveryMethods: List[str]
    unitItems: List[UnitItemTicket]
    contact: Optional[Contact] = None
    utcHoldExpiration: Optional[datetime] = None
    utcConfirmedAt: Optional[datetime] = None
    utcDeliveredAt: Optional[datetime] = None
    resellerReference: Optional[str] = None
    supplierReference: Optional[str] = None
    refreshFrequency: Optional[str] = None
    voucher: Optional[Ticket] = None
    cancellationRequest: Optional[CancellationRequest] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


@dataclass
class BookingConfirmationRequest(BaseModel):
    contact: Contact
    resellerReference: Optional[str] = None
    extra_fields: Optional[dict] = field(default_factory=dict)


class CancelReason(Enum):
    # is the most common and indicates that the customer requested the cancellation
    CUSTOMER = 'CUSTOMER'

    # indicates that the supplier requested the cancellation
    # (possibly due to bad weather or other unexpected circumstances)
    SUPPLIER = 'SUPPLIER'

    # indicates that the booking cancellation is being requested by the Reseller
    # because it has been determined the booking was fraudulent
    FRAUD = 'FRAUD'

    # indicates that the cancellation reason does not fall into one of these categories.
    # This SHOULD be used only in rare circumstances
    OTHER = 'OTHER'
