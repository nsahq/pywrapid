#!/usr/bin/python3
"""
Collection of helper functions
"""
from copy import deepcopy
from typing import Optional


def dict_merge(
    base: dict, data: dict, path: Optional[list] = None, raise_on_conflict: bool = False
) -> dict:
    """Recursive merge of dict objects into new dict

    The merge will make a deep copy of the base dict and merge the data dict into it.
    It will not modify the base dict being passed in.

    If the same key exists in base and data, the value from data will be used unless
    raise_on_conflict is True, in which case a ValueError will be raised.

    Args:
        base (dict): The base dict to merge into
        data (dict): The data dict to merge into base
        path (list, optional): _description_. Defaults to None.
        raise_on_conflict (bool): Raise on conflict instead of overwriting base

    Raises:
        ValueError: Raised on leaf conflict when raise_on_conflict is True

    Returns: Merged dict
    """
    copy = deepcopy(base)
    if path is None:
        path = []
    for key in data:
        if key in copy:
            if isinstance(copy[key], dict) and isinstance(data[key], dict):
                copy[key] = dict_merge(
                    copy[key],
                    data[key],
                    path=path + [str(key)],
                    raise_on_conflict=raise_on_conflict,
                )
            elif data[key] is None:
                continue
            elif copy[key] == data[key]:
                continue  # same leaf value, skip traversal if children are the same
            else:
                if raise_on_conflict:
                    raise ValueError(f"Conflict at {'.'.join(path + [str(key)])}")
                copy[key] = data[key]
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

    missed = []
    for key in expected_keys:
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
