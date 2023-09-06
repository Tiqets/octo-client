from typing import List, Union

from octo_client.const import PRIVATE_DATA_KEYS, PRIVATE_DATA_REPLACEMENT


def hide_sensitive_data(
    data: Union[str, list, dict], keys: List[str] = PRIVATE_DATA_KEYS
) -> Union[str, list, dict]:
    """
    Hide sensitive data from a nested dict by doing a partial match on the keys.
    data: dict to be filtered
    keys: list of keys to be filtered
    """
    if isinstance(data, str):
        return data

    if isinstance(data, list):
        return [hide_sensitive_data(item, keys) for item in data]

    if isinstance(data, dict):
        for k, v in data.items():
            hide_sensitive_data(v, keys)

            for key in keys:
                if key in k.lower():
                    data[k] = PRIVATE_DATA_REPLACEMENT
    return data
