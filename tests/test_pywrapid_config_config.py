#!/usr/bin/python3
"""Pywrapid config tests"""

import os
import pathlib

import pytest

import pywrapid.config.config as module_0
import pywrapid.config.exceptions as module_1

cwd = pathlib.Path().resolve()


def test_case_0() -> None:
    """Raise config error on missing keys"""
    wrapid_config_0 = module_0.WrapidConfig()
    with pytest.raises(module_1.ConfigurationError):
        wrapid_config_0.validate_keys(wrapid_config_0)


def test_case_1() -> None:
    """Faulty file type"""
    bool_0 = True
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        module_0.ApplicationConfig(file_type=bool_0, allow_config_discovery=bool_0)


def test_case_2() -> None:
    """Missing configuration file"""
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = os.path.abspath(__file__)
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        wrapid_config_0.application_config_location(str_0)


def test_case_3() -> None:
    """Missing parameters"""
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        module_0.ApplicationConfig()


def test_case_4() -> None:
    """Fail setup with discovery"""
    str_0 = 'Wk;pMX=x)48K$$"'
    application_config_0 = module_0.ApplicationConfig(str_0, str_0, str_0)
    assert (
        f"{type(application_config_0).__module__}.{type(application_config_0).__qualname__}"
        == "pywrapid.config.config.ApplicationConfig"
    )
    assert application_config_0.config_path == 'Wk;pMX=x)48K$$"'
    assert application_config_0.cfg == {}
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        module_0.ApplicationConfig(application_name=str_0, allow_config_discovery=True)


def test_case_5() -> None:
    """Missing subsection param"""
    wrapid_config_0 = module_0.WrapidConfig()
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(wrapid_config_0)


def test_case_6() -> None:
    """String not WrapidConfig"""
    str_0 = "4"
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(str_0, str_0)


def test_case_7() -> None:
    """Base init"""
    module_0.WrapidConfig()


def test_case_8() -> None:
    """Non-usable file"""
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = "A$-{HrE55"
    wrapid_config_0.is_file_usable(str_0)
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(wrapid_config_0)


def test_case_9() -> None:
    """Missing subsection in config"""
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = "W9C#"
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(wrapid_config_0, str_0)


def test_case_10() -> None:
    """Config loading"""
    wrapid_config_0 = module_0.ApplicationConfig(config_path=f"{cwd}/tests/test_conf_ok.yml")
    assert isinstance(wrapid_config_0, module_0.ApplicationConfig)
    assert "logging" in wrapid_config_0.cfg

    wrapid_config_1 = module_0.ConfigSubSection(wrapid_config_0, "logging")
    assert isinstance(wrapid_config_1, module_0.ConfigSubSection)
    assert "default" in wrapid_config_1.cfg


def test_case_11() -> None:
    """Correct dict config type in subconfig"""
    str_0 = "randomstr0"
    str_1 = "randomstr1"
    dict_0 = {str_0: {str_1: str_1}}
    wrapid_config_0 = module_0.ConfigSubSection(conf=dict_0, subsection=str_0)
    assert str_1 in wrapid_config_0.cfg


def test_case_12() -> None:
    """Missing section in dict config type in subconfig"""
    str_0 = "randomstr0"
    str_1 = "randomstr1"
    dict_0 = {"missed_level": {str_1: str_1}}
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(conf=dict_0, subsection=str_0)
