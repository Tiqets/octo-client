from dataclasses import asdict, dataclass
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from dacite import Config, from_dict


class BaseModel:

    @staticmethod
    def _datetime_from_iso_format(datetime_str: Optional[str]) -> Optional[datetime]:
        if datetime_str:
            return datetime.fromisoformat(datetime_str.replace('Z', '+00:00'))
        return None

    def as_dict(self) -> dict:
        """
        Dumps dataclass into dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict, config=None):
        """
        Populating data class from a dictionary with strict type checking.
        """
        if config is None:
            config = Config(type_hooks={
                date: date.fromisoformat,
                datetime: cls._datetime_from_iso_format,
            })
        return from_dict(data_class=cls, data=data, config=config)


@dataclass
class SupplierContact(BaseModel):
    email: str
    address: Optional[str] = None
    telephone: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


@dataclass
class Supplier(BaseModel):
    id: str
    name: str
    endpoint: str
    contact: SupplierContact


@dataclass
class Capability(BaseModel):
    id: str
    revision: int
    required: bool


@dataclass
class Unit(BaseModel):
    id: str
    internalName: str
    type: str
    reference: Optional[str] = None


@dataclass
class Option(BaseModel):
    id: str
    internalName: str
    units: List[Unit]
    reference: Optional[str] = None


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
    capabilities: List[Capability]
    options: List[Option]
    reference: Optional[str] = None


@dataclass
class AvailabilityCalendarItem(BaseModel):
    localDate: date
    status: str
    vacancies: Optional[int] = None


@dataclass
class AvailabilityItem(BaseModel):
    id: str
    localDateTimeStart: datetime
    localDateTimeEnd: datetime
    status: str
    vacancies: Optional[int] = None


@dataclass
class UnitItem(BaseModel):
    uuid: str
    unitId: str
    resellerReference: Optional[str] = None


@dataclass
class UnitQuantity(BaseModel):
    unitId: str
    quantity: int


@dataclass
class BookingRequest(BaseModel):
    uuid: str
    productId: str
    optionId: str
    availabilityId: str
    unitItems: List[UnitItem]
    holdExpirationMinutes: Optional[int] = None
    resellerReference: Optional[str] = None


@dataclass
class Availability(BaseModel):
    id: str
    localDateTimeStart: datetime
    localDateTimeEnd: datetime


@dataclass
class Contact(BaseModel):
    locales: List[str]
    fullName: Optional[str] = None
    emailAddress: Optional[str] = None
    phoneNumber: Optional[str] = None
    country: Optional[str] = None


@dataclass
class DeliveryOption(BaseModel):
    deliveryFormat: str
    deliveryValue: str


@dataclass
class Ticket(BaseModel):
    deliveryOptions: List[DeliveryOption]
    redemptionMethod: str
    utcDeliveredAt: Optional[datetime] = None
    utcRedeemedAt: Optional[datetime] = None


@dataclass
class BookingTicket(BaseModel):
    deliveryOptions: List[DeliveryOption]
    redemptionMethod: str
    utcDeliveredAt: Optional[datetime] = None
    utcRedeemedAt: Optional[datetime] = None


@dataclass
class UnitItemTicket(BaseModel):
    uuid: str
    unitId: str
    ticket: Optional[BookingTicket] = None
    resellerReference: Optional[str] = None
    supplierReference: Optional[str] = None


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
    resellerReference: Optional[str] = None
    supplierReference: Optional[str] = None
    refreshFrequency: Optional[str] = None
    voucher: Optional[Ticket] = None
    cancellationRequest: Optional[CancellationRequest] = None


@dataclass
class BookingConfirmationRequest(BaseModel):
    contact: Contact
    resellerReference: Optional[str] = None


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
