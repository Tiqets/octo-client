from typing import List, Union

from octo_client.const import PRIVATE_DATA_KEYS, PRIVATE_DATA_REPLACEMENT


def hide_sensitive_data(
    data: Union[str, dict], keys: List[str] = PRIVATE_DATA_KEYS
) -> Union[str, dict]:
    """
    Hide sensitive data from a nested dict by doing a partial match on the keys.
    data: dict to be filtered
    keys: list of keys to be filtered
    """
    if isinstance(data, str):
        return data

    for k, v in data.items():
        if isinstance(v, dict):
            hide_sensitive_data(v, keys)

        for key in keys:
            if key in k.lower():
                data[k] = PRIVATE_DATA_REPLACEMENT
    return data
