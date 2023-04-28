#!/usr/bin/python3
"""Pywrapid config tests"""

import os
import pathlib

import pytest

import pywrapid.config.config as module_0
import pywrapid.config.exceptions as module_1

cwd = pathlib.Path().resolve()


# pylint: disable=redefined-outer-name
@pytest.fixture()
def fixture_yaml_file_0(tmp_path: str) -> str:
    """Fixture for producing sample yaml config file"""
    # Top level
    path_0 = tmp_path / "sample.yml"  # type: ignore
    path_0.touch()
    path_0.write_text(
        """a: "aaa"
b:
  c: "ccc"
  d: "ddd"
e:
  - "hello"
  - "world"
"""
    )

    return os.path.abspath(f"{tmp_path}/sample.yml")


@pytest.fixture()
def fixture_yaml_file_1(tmp_path: str) -> str:
    """Fixture for producing sample yaml config file"""
    # Top level
    path_0 = tmp_path / "sample.yml"  # type: ignore
    path_0.touch()
    path_0.write_text(
        """I am
n:ot
    even close
to being valid
=
$
"""
    )

    return os.path.abspath(f"{tmp_path}/sample.yml")


def test_config_wrapidconfig_0() -> None:
    """Validating: WrapidConfig failed validation"""
    wrapid_config_0 = module_0.WrapidConfig()
    wrapid_config_0.cfg = {"aa": 1, "bb": 2}
    with pytest.raises(module_1.ConfigurationValidationError):
        wrapid_config_0.validate_keys(["a"])


def test_config_wrapidconfig_1() -> None:
    """Validating: missed required wrapid config raises error"""
    wrapid_config_0 = module_0.WrapidConfig()
    wrapid_config_0.cfg = {}
    with pytest.raises(module_1.ConfigurationError):
        wrapid_config_0.validate_keys(["a"])


def test_config_wrapidconfig_2() -> None:
    """Validating: WrapidConfig successful validation"""
    wrapid_config_0 = module_0.WrapidConfig()
    wrapid_config_0.cfg = {"a": 1, "b": 2}
    assert wrapid_config_0.validate_keys(["a"]) is True


def test_config_wrapidconfig_3() -> None:
    """Validating: missed required wrapid config raises error"""
    wrapid_config_0 = module_0.WrapidConfig()
    with pytest.raises(module_1.ConfigurationError):
        wrapid_config_0.validate_keys(["a"])


def test_config_wrapidconfig_4() -> None:
    """Raise config error on missing keys"""
    wrapid_config_0 = module_0.WrapidConfig()
    with pytest.raises(module_1.ConfigurationError):
        wrapid_config_0.validate_keys(wrapid_config_0)


def test_config_wrapidconfig_5() -> None:
    """Missed application config for wrapidconfig"""
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = os.path.abspath(__file__)
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        wrapid_config_0.application_config_location(str_0)


def test_config_wrapidconfig_6() -> None:
    """Missing subsection param"""
    wrapid_config_0 = module_0.WrapidConfig()
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(wrapid_config_0)


def test_config_wrapidconfig_8() -> None:
    """Base init"""
    module_0.WrapidConfig()


def test_config_wrapidconfig_9() -> None:
    """Non-usable file"""
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = "A$-{HrE55"
    wrapid_config_0.is_file_usable(str_0)
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(wrapid_config_0)


def test_config_wrapidconfig_10(fixture_yaml_file_0: str) -> None:
    """Valid application config for wrapidconfig"""
    wrapid_config_0 = module_0.ApplicationConfig(
        "tmp", config_path=fixture_yaml_file_0, allow_config_discovery=False
    )
    str_0 = wrapid_config_0.application_config_location("tmp", locations=[fixture_yaml_file_0])
    assert str_0 == fixture_yaml_file_0


def test_config_applicationconfig_0() -> None:
    """Faulty file type"""
    bool_0 = True
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        module_0.ApplicationConfig(file_type=bool_0, allow_config_discovery=bool_0)


def test_config_applicationconfig_1() -> None:
    """Missing parameters"""
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        module_0.ApplicationConfig()


def test_config_applicationconfig_2() -> None:
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


def test_config_applicationconfig_3() -> None:
    """Config loading"""
    wrapid_config_0 = module_0.ApplicationConfig(config_path=f"{cwd}/tests/test_conf_ok.yml")
    assert isinstance(wrapid_config_0, module_0.ApplicationConfig)
    assert "logging" in wrapid_config_0.cfg

    wrapid_config_1 = module_0.ConfigSubSection(wrapid_config_0, "logging")
    assert isinstance(wrapid_config_1, module_0.ConfigSubSection)
    assert "default" in wrapid_config_1.cfg


def test_config_configsubsection_0() -> None:
    """String not WrapidConfig"""
    str_0 = "4"
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(str_0, str_0)


def test_config_configsubsection_1() -> None:
    """Missing subsection in config"""
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = "W9C#"
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(wrapid_config_0, str_0)


def test_config_configsubsection_2() -> None:
    """Correct dict config type in subconfig"""
    str_0 = "randomstr0"
    str_1 = "randomstr1"
    dict_0 = {str_0: {str_1: str_1}}
    wrapid_config_0 = module_0.ConfigSubSection(conf=dict_0, subsection=str_0)
    assert str_1 in wrapid_config_0.cfg


def test_config_configsubsection_3() -> None:
    """Missing section in dict config type in subconfig"""
    str_0 = "randomstr0"
    str_1 = "randomstr1"
    dict_0 = {"missed_level": {str_1: str_1}}
    with pytest.raises(module_0.ConfigurationError):
        module_0.ConfigSubSection(conf=dict_0, subsection=str_0)


def test_config_configsubsection_4() -> None:
    """Validating empty wrapid config raises error"""
    wrapid_config_0 = module_0.ConfigSubSection({"a": {}}, "a")
    with pytest.raises(module_1.ConfigurationError):
        wrapid_config_0.validate_keys(["a"])


def test_config_applicationconfig_yaml_config_to_dict_0(fixture_yaml_file_0: str) -> None:
    """Test yaml config to dict"""
    cfg_0 = module_0.ApplicationConfig("tmp", config_path=fixture_yaml_file_0)
    dict_0 = cfg_0.cfg
    assert isinstance(dict_0, dict)
    assert "a" in dict_0
    assert isinstance(dict_0["a"], str)
    assert isinstance(dict_0["b"], dict)
    assert isinstance(dict_0["e"], list)
    assert "hello" in dict_0["e"]
    assert "world" in dict_0["e"]
    assert "c" in dict_0["b"]
    assert "d" in dict_0["b"]
    assert isinstance(dict_0["b"]["c"], str)
    assert isinstance(dict_0["b"]["d"], str)


def test_config_applicationconfig_yaml_config_to_dict_1() -> None:
    """Test yaml config raise on missing config"""
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        module_0.ApplicationConfig(
            "tmp", config_path="does not exist", allow_config_discovery=False
        )


def test_config_applicationconfig_yaml_config_to_dict_3(fixture_yaml_file_0: str) -> None:
    """Test yaml config to dict for missed validation"""
    cfg_0 = module_0.ApplicationConfig("tmp", config_path=fixture_yaml_file_0)
    with pytest.raises(module_1.ConfigurationValidationError):
        module_0.ApplicationConfig.yaml_config_to_dict(
            cfg_0, config=fixture_yaml_file_0, expected_keys=["notreal"]
        )


def test_config_applicationconfig_yaml_config_to_dict_4(fixture_yaml_file_1: str) -> None:
    """Test yaml config to dict for bad yaml format"""
    with pytest.raises(module_1.ConfigurationValidationError):
        module_0.ApplicationConfig("tmp", config_path=fixture_yaml_file_1)
