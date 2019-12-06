from dataclasses import asdict, dataclass
from typing import Optional

from dacite import from_dict


class BaseModel:

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
        return from_dict(data_class=cls, data=data, config=config)


@dataclass
class SupplierContact(BaseModel):
    address: str
    email: Optional[str] = None
    telephone: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


@dataclass
class Supplier(BaseModel):
    id: str
    name: str
    endpoint: str
    contact: SupplierContact
