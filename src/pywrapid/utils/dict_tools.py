#!/usr/bin/python3
"""
Collection of helper functions
"""
from copy import deepcopy


def dict_merge(base: dict, data: dict, path: list = None) -> dict:
    """Recursive merge of dict objects

    Args:
        base (dict): _description_
        data (dict): _description_
        path (list, optional): _description_. Defaults to None.

    Raises:
        ValueError: Raised on leaf conflict

    Returns: Merged dict
    """
    copy = deepcopy(base)
    if path is None:
        path = []
    for key in data:
        if key in copy:
            if isinstance(copy[key], dict) and isinstance(data[key], dict):
                dict_merge(copy[key], data[key], path + [str(key)])
            elif copy[key] == data[key]:
                pass  # same leaf value
            else:
                raise ValueError(f"Conflict at {'.'.join(path + [str(key)])}")
        else:
            copy[key] = data[key]
    return copy


def dict_keys_exist(
    data: dict,
    expected_keys: list,
    allow_empty: bool = False,
    raise_on_fail: bool = True,
) -> bool:
    """Validates if expected keys exist (optionally; and has data) in a given dict.

    Args:
        data (dict): The dict to run validation on.
        expected_keys (list): List of keys that should exist.
        allow_empty (bool, optional): Is key object allowed to have empty value.
        raise_on_fail (bool, optional): Raise if validation fails.

    Raises:
        ValueError: Raised on all validation errors when raise_on_fail = True.

    Returns:
        bool: True when validation is passed.
    """
    if not expected_keys:
        if raise_on_fail:
            raise ValueError("No expected values supplied")
        return False

    for key in expected_keys:
        missed = []
        if key not in data:
            missed.append(key)
        elif data[key] in ["", (), [], {}, None] and allow_empty is False:
            if raise_on_fail:
                raise ValueError(f"Empty value in: {key}")
            return False

    if len(missed) > 0:
        if raise_on_fail:
            raise ValueError(f"Missing expected items: {missed}")
        return False

    return True
