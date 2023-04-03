from dataclasses import asdict, dataclass, field
from datetime import date, datetime, time
from typing import List, Optional

from tonalite.config import Config
from tonalite.core import from_dict

from octo_client import const


@dataclass
class BaseModel:
    @staticmethod
    def _datetime_from_iso_format(datetime_str: Optional[str]) -> Optional[datetime]:
        if datetime_str:
            return datetime.fromisoformat(datetime_str.replace("Z", "+00:00"))
        return None

    def as_dict(self) -> dict:
        """
        Dumps dataclass into dictionary.
        """
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        """
        Populating data class from a dictionary with strict type checking.
        """
        if config is None:
            config = Config(
                strict=strict,
                type_hooks={
                    date: date.fromisoformat,
                    datetime: cls._datetime_from_iso_format,
                },
            )
        return from_dict(cls, data=data, config=config)


@dataclass
class SupplierContact(BaseModel):
    website: Optional[str] = None
    email: Optional[str] = None
    telephone: Optional[str] = None
    address: Optional[str] = None


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
class UnitRestrictions(BaseModel):
    minAge: int
    maxAge: int
    idRequired: bool
    paxCount: int
    accompaniedBy: List[str] = field(default_factory=list)
    minQuantity: Optional[int] = None
    maxQuantity: Optional[int] = None


@dataclass
class Unit(BaseModel):
    id: str
    internalName: str
    type: const.UnitType
    restrictions: UnitRestrictions
    requiredContactFields: List[const.RequiredContactField] = field(default_factory=list)
    reference: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                cast=[
                    const.UnitType,
                    const.RequiredContactField,
                ],
            ),
        )


@dataclass
class OptionRestriction(BaseModel):
    minUnits: Optional[int] = None
    maxUnits: Optional[int] = None


@dataclass
class Option(BaseModel):
    id: str
    default: bool
    internalName: str
    cancellationCutoff: str
    cancellationCutoffAmount: int
    cancellationCutoffUnit: const.CancellationCutoffUnit
    restrictions: OptionRestriction
    reference: Optional[str] = None
    availabilityLocalStartTimes: List[str] = field(default_factory=list)
    requiredContactFields: List[const.RequiredContactField] = field(default_factory=list)
    units: List[Unit] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                cast=[
                    const.CancellationCutoffUnit,
                    const.RequiredContactField,
                ],
            ),
        )


@dataclass
class Product(BaseModel):
    id: str
    internalName: str
    locale: str
    timeZone: str
    allowFreesale: bool
    instantConfirmation: bool
    instantDelivery: bool
    availabilityRequired: bool
    availabilityType: const.AvailabilityType
    redemptionMethod: const.RedemptionMethod
    options: List[Option]
    deliveryFormats: List[const.DeliveryFormat] = field(default_factory=list)
    deliveryMethods: List[const.DeliveryMethod] = field(default_factory=list)
    reference: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                cast=[
                    const.AvailabilityType,
                    const.RedemptionMethod,
                    const.DeliveryFormat,
                    const.DeliveryMethod,
                ],
            ),
        )


@dataclass
class OpeningHours(BaseModel):
    from_: time
    to: time

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        # renaming the keyword
        data["from_"] = data.pop("from")
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(strict=strict, type_hooks={time: time.fromisoformat}),
        )


@dataclass
class AvailabilityCalendarItem(BaseModel):
    localDate: date
    available: bool
    status: const.AvailabilityStatus
    vacancies: Optional[int] = None
    capacity: Optional[int] = None
    openingHours: List[OpeningHours] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                type_hooks={
                    date: date.fromisoformat,
                },
                cast=[
                    const.AvailabilityStatus,
                ],
            ),
        )


@dataclass
class Availability(BaseModel):
    id: str
    localDateTimeStart: datetime
    localDateTimeEnd: datetime
    allDay: bool
    available: bool
    status: const.AvailabilityStatus
    utcCutoffAt: datetime
    openingHours: List[OpeningHours] = field(default_factory=list)
    vacancies: Optional[int] = None
    capacity: Optional[int] = None
    maxUnits: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                type_hooks={
                    datetime: cls._datetime_from_iso_format,
                },
                cast=[
                    const.AvailabilityStatus,
                ],
            ),
        )


@dataclass
class UnitItem(BaseModel):
    unitId: str
    uuid: Optional[str] = None


@dataclass
class BookingContact(BaseModel):
    locales: List[str] = field(default_factory=list)
    fullName: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    emailAddress: Optional[str] = None
    phoneNumber: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    notes: Optional[str] = None


@dataclass
class ConfirmationUnitItem(BaseModel):
    unitId: str
    uuid: Optional[str] = None
    resellerReference: Optional[str] = None
    contact: Optional[BookingContact] = None


@dataclass
class UnitQuantity(BaseModel):
    id: str
    quantity: int


@dataclass
class DeliveryOption(BaseModel):
    deliveryFormat: const.DeliveryFormat
    deliveryValue: str

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                cast=[
                    const.DeliveryFormat,
                ],
            ),
        )


@dataclass
class Ticket(BaseModel):
    redemptionMethod: const.RedemptionMethod
    utcRedeemedAt: Optional[datetime] = None
    deliveryOptions: List[DeliveryOption] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                type_hooks={
                    datetime: cls._datetime_from_iso_format,
                },
                cast=[
                    const.RedemptionMethod,
                ],
            ),
        )


@dataclass
class BookingUnitItem(BaseModel):
    uuid: str
    unitId: str
    unit: Unit
    status: const.BookingStatus
    contact: BookingContact
    resellerReference: Optional[str] = None
    supplierReference: Optional[str] = None
    utcRedeemedAt: Optional[datetime] = None
    ticket: Optional[Ticket] = None

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                type_hooks={
                    datetime: cls._datetime_from_iso_format,
                },
                cast=[
                    const.BookingStatus,
                ],
            ),
        )


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
class Cancellation(BaseModel):
    refund: const.Refund
    reason: Optional[str] = None
    utcCancelledAt = datetime

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                type_hooks={
                    datetime: cls._datetime_from_iso_format,
                },
                cast=[
                    const.Refund,
                ],
            ),
        )


@dataclass
class BookingAvailability(BaseModel):
    id: str
    localDateTimeStart: datetime
    localDateTimeEnd: datetime
    allDay: bool
    openingHours: List[OpeningHours] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                type_hooks={
                    datetime: cls._datetime_from_iso_format,
                },
            ),
        )


@dataclass
class Booking(BaseModel):
    id: str
    uuid: str
    testMode: bool
    status: const.BookingStatus
    productId: str
    product: Product
    optionId: str
    option: Option
    cancellable: bool
    freesale: bool
    availabilityId: str
    availability: BookingAvailability
    contact: BookingContact
    notes: Optional[str] = None
    voucher: Optional[Ticket] = None
    resellerReference: Optional[str] = None
    supplierReference: Optional[str] = None
    utcCreatedAt: Optional[datetime] = None
    utcUpdatedAt: Optional[datetime] = None
    utcExpiresAt: Optional[datetime] = None
    utcRedeemedAt: Optional[datetime] = None
    utcConfirmedAt: Optional[datetime] = None
    cancellation: Optional[Cancellation] = None
    deliveryMethods: List[const.DeliveryMethod] = field(default_factory=list)
    unitItems: List[BookingUnitItem] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, config: Optional[Config] = None, strict: bool = False):
        return from_dict(
            data_class=cls,
            data=data,
            config=Config(
                strict=strict,
                type_hooks={
                    datetime: cls._datetime_from_iso_format,
                },
                cast=[
                    const.BookingStatus,
                    const.DeliveryMethod,
                ],
            ),
        )
