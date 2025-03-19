from typing import Any, Dict


def update_dict_value(dict: Dict[str, Any], key: str, index: int, value: Any):
    """
    Update the value of the given dictionary with the specified key.
    If the target is a list and index is provided, update the list element at the given index
    """
    if isinstance(dict.get(key), list) and index is not None:
        if 0 <= index < len(dict[key]) or index == -1:
            dict[key][index] = value
        else:
            raise IndexError(f"Index {index} out of range for list at {key}.")
    else:
        dict[key] = value
