# Automatically generated by Pynguin.
import os

import pytest

import pywrapid.config.config as module_0
import pywrapid.config.exception as module_1


def test_case_0():
    wrapid_config_0 = module_0.WrapidConfig()
    with pytest.raises(module_1.ConfigurationError):
        wrapid_config_0.validate_keys(wrapid_config_0)


@pytest.mark.xfail(strict=True)
def test_case_1():
    bool_0 = True
    module_0.ApplicationConfig(file_type=bool_0, allow_config_discovery=bool_0)


def test_case_2():
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = os.path.abspath(__file__)
    with pytest.raises(module_1.ConfigurationFileNotFoundError):
        wrapid_config_0.application_config_location(str_0)


@pytest.mark.xfail(strict=True)
def test_case_3():
    module_0.ApplicationConfig()


@pytest.mark.xfail(strict=True)
def test_case_4():
    str_0 = 'Wk;pMX=x)48K$$"'
    application_config_0 = module_0.ApplicationConfig(str_0, str_0, str_0)
    assert (
        f"{type(application_config_0).__module__}.{type(application_config_0).__qualname__}"
        == "pywrapid.config.config.ApplicationConfig"
    )
    assert application_config_0.config_path == 'Wk;pMX=x)48K$$"'
    assert application_config_0.cfg == {}
    module_0.ApplicationConfig()


def test_case_5():
    wrapid_config_0 = module_0.WrapidConfig()
    with pytest.raises(ValueError):
        module_0.ConfigSubSection(wrapid_config_0)


@pytest.mark.xfail(strict=True)
def test_case_6():
    str_0 = "4"
    module_0.ConfigSubSection(str_0, str_0)


def test_case_7():
    wrapid_config_0 = module_0.WrapidConfig()


def test_case_8():
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = "A$-{HrE55"
    bool_0 = wrapid_config_0.is_file_usable(str_0)
    with pytest.raises(ValueError):
        module_0.ConfigSubSection(wrapid_config_0)


def test_case_9():
    wrapid_config_0 = module_0.WrapidConfig()
    str_0 = "W9C#"
    with pytest.raises(ValueError):
        module_0.ConfigSubSection(wrapid_config_0, str_0)