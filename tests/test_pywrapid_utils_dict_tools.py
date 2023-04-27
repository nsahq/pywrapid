#!/usr/bin/python3
"""Pywrapid dict tools tests"""

import os

import pytest

import pywrapid.utils.dict_tools as module_0

# pylint: disable=redefined-outer-name, protected-access

def test_utils_dict_tools_dict_merge_0():
    """Test dict_merge"""
    base = {"a": 1, "b": {"c": 2, "d": 3}}
    data = {"b": {"c": 4, "e": 5}, "f": 6}
    expected = {"a": 1, "b": {"c": 4, "d": 3, "e": 5}, "f": 6}
    assert module_0.dict_merge(base, data) == expected


def test_utils_dict_tools_dict_keys_exist_0():
    """Test dict_keys_exist"""
    data = {"a": 1, "b": {"c": 2, "d": 3}, "e": ["hello", "world"]}
    expected_keys = ["a", "b", "e"]
    assert module_0.dict_keys_exist(data, expected_keys, raise_on_fail=False) is True


def test_utils_dict_tools_dict_keys_exist_1():
    """Test dict_keys_exist with too many keys expected"""
    data = {"a": 1, "b": {"c": 2, "d": 3}, "e": ["hello", "world"]}
    expected_keys = ["a", "b", "c", "d"]
    assert module_0.dict_keys_exist(data, expected_keys, raise_on_fail=False) is False


def test_utils_dict_tools_dict_keys_exist_2():
    """Test dict_keys_exist to not allow partial matches"""
    data = {"aa": 1, "b": {"c": 2, "d": 3}, "e": ["hello", "world"]}
    expected_keys = ["a", "b", "e"]
    assert module_0.dict_keys_exist(data, expected_keys, raise_on_fail=False) is False


def test_utils_dict_tools_dict_keys_exist_3():
    """Test dict_keys_exist to raise on partial matches"""
    data = {"a": 1, "b": {"c": 2, "d": 3}, "e": ["hello", "world"]}
    expected_keys = ["a", "b", "c", "e"]
    with pytest.raises(ValueError):
        module_0.dict_keys_exist(data, expected_keys, raise_on_fail=True)


def test_utils_dict_tools_dict_keys_exist_4():
    """Test dict_keys_exist to raise on partial matches"""
    data = {"a": 1, "b": {"c": 2, "d": 3}, "e": []}
    expected_keys = ["a", "b", "e"]
    with pytest.raises(ValueError):
        module_0.dict_keys_exist(data, expected_keys, raise_on_fail=True)
