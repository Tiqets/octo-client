from enum import Enum


class UnitType(Enum):
    ADULT = "ADULT"
    YOUTH = "YOUTH"
    CHILD = "CHILD"
    INFANT = "INFANT"
    FAMILY = "FAMILY"
    SENIOR = "SENIOR"
    STUDENT = "STUDENT"
    MILITARY = "MILITARY"
    OTHER = "OTHER"


class RequiredContactField(Enum):
    firstName = "firstName"
    lastName = "lastName"
    emailAddress = "emailAddress"
    phoneNumber = "phoneNumber"
    country = "country"
    notes = "notes"
    locales = "locales"


class CancellationCutoffUnit(Enum):
    hour = "hour"
    minute = "minute"
    day = "day"


class AvailabilityType(Enum):
    START_TIME = "START_TIME"
    OPENING_HOURS = "OPENING_HOURS"


class DeliveryFormat(Enum):
    PDF_URL = "PDF_URL"
    QRCODE = "QRCODE"
    PKPASS_URL = "PKPASS_URL"  # VENTRATA ONLY
    CODE128 = "CODE128"  # VENTRATA ONLY


class DeliveryMethod(Enum):
    VOUCHER = "VOUCHER"
    TICKET = "TICKET"


class RedemptionMethod(Enum):
    DIGITAL = "DIGITAL"
    PRINT = "PRINT"
    MANIFEST = "MANIFEST"


class AvailabilityStatus(Enum):
    AVAILABLE = "AVAILABLE"
    FREESALE = "FREESALE"
    SOLD_OUT = "SOLD_OUT"
    LIMITED = "LIMITED"
    CLOSED = "CLOSED"


class BookingStatus(Enum):
    ON_HOLD = "ON_HOLD"
    CONFIRMED = "CONFIRMED"
    EXPIRED = "EXPIRED"
    CANCELLED = "CANCELLED"
    REDEEMED = "REDEEMED"
    PENDING = "PENDING"
    REJECTED = "REJECTED"


class Refund(Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    NONE = "NONE"


class CancelReason(Enum):
    # is the most common and indicates that the customer requested the cancellation
    CUSTOMER = "CUSTOMER"

    # indicates that the supplier requested the cancellation
    # (possibly due to bad weather or other unexpected circumstances)
    SUPPLIER = "SUPPLIER"

    # indicates that the booking cancellation is being requested by the Reseller
    # because it has been determined the booking was fraudulent
    FRAUD = "FRAUD"

    # indicates that the cancellation reason does not fall into one of these categories.
    # This SHOULD be used only in rare circumstances
    OTHER = "OTHER"
