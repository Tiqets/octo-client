from dataclasses import is_dataclass
from typing import Any, Type

from dacite import Config
from dacite.core import _build_value_for_collection, _build_value_for_union
from dacite.data import Data
from dacite.types import extract_origin_collection, is_generic_collection, is_instance, is_union


def _build_value(type_: Type, data: Any, config: Config) -> Any:
    if is_union(type_):
        return _build_value_for_union(union=type_, data=data, config=config)
    elif is_generic_collection(type_) and is_instance(data, extract_origin_collection(type_)):
        return _build_value_for_collection(collection=type_, data=data, config=config)
    elif is_dataclass(type_) and is_instance(data, Data):
        # modification: using from_dict from model instead of the generic one
        return type_.from_dict(data)
    return data
