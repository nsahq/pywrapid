#!/usr/bin/python3
"""Pywrapid log tests"""

import logging
import pathlib
from contextlib import contextmanager
from typing import Generator

import pytest
from _pytest.fixtures import SubRequest
from _pytest.logging import LogCaptureHandler

import pywrapid.config.config as module_0
import pywrapid.log as module_1

# pylint: disable=redefined-outer-name, protected-access

cwd = pathlib.Path().resolve()
real_log_file_0 = f"{cwd}/tests/test.log"


@contextmanager
def catch_logs(level: int, logger: logging.Logger) -> Generator:
    """Context manager that sets the level for capturing of logs.

    After the end of the 'with' statement the level is restored to its original value.

    :param level: The level.
    :param logger: The logger to update.
    """
    handler = LogCaptureHandler()
    orig_level = logger.level
    logger.setLevel(level)
    logger.addHandler(handler)
    try:
        yield handler
    finally:
        logger.setLevel(orig_level)
        logger.removeHandler(handler)


@pytest.fixture()
def log_fixture_0(request: SubRequest, caplog: pytest.LogCaptureFixture) -> list:
    """Fixture for producing log file"""
    file_0 = f"{cwd}/tests/test_conf_ok.yml"
    logger_0 = request.node.name
    wrapid_config_0 = module_0.ApplicationConfig(config_path=file_0)
    assert isinstance(wrapid_config_0, module_0.ApplicationConfig)
    wrapid_config_1 = module_0.ConfigSubSection(wrapid_config_0, "logging")
    assert isinstance(wrapid_config_1, module_0.ConfigSubSection)
    caplog.clear()
    log_0 = logging.getLogger(logger_0)
    module_1.application_logging(wrapid_config_1)
    log_level = wrapid_config_1.cfg[request.node.name]["console"]["level"]
    if log_level == 0:
        log_level = 60
    with catch_logs(level=log_level, logger=log_0) as handler:
        log_0.debug("debug_message")
        log_0.info("info_message")
        log_0.warning("warning_message")
        log_0.error("error_message")
        log_0.critical("critical_message")

        return [(r.name, r.levelno, r.getMessage()) for r in handler.records]


def test_case_0() -> None:
    """Config load config"""
    file_0 = f"{cwd}/tests/test_conf_ok.yml"

    wrapid_config_0 = module_0.ApplicationConfig(config_path=file_0)
    assert isinstance(wrapid_config_0, module_0.ApplicationConfig)

    wrapid_config_1 = module_0.ConfigSubSection(wrapid_config_0, "logging")
    assert isinstance(wrapid_config_1, module_0.ConfigSubSection)

    assert wrapid_config_1.cfg["default"] == {
        "file": {
            "level": 0,
            "location": "tests/test.log",
        },
        "console": {
            "level": 20,
        },
    }

    module_1.application_logging(wrapid_config_1)


def test_case_1() -> None:
    """byte type"""
    bytes_0 = b""
    with pytest.raises(Exception):
        module_1.application_logging(bytes_0)


def test_case_2() -> None:
    """Empty dict"""
    dict_0: dict = {}
    module_1.application_logging(dict_0)
    module_1._generate_default(dict_0)


def test_case_3() -> None:
    """Set up random logger with defaults"""
    str_0 = "somerandomtext"
    dict_0 = {str_0: None}
    module_1.application_logging(dict_0)


def test_case_4(log_fixture_0: list, request: SubRequest) -> None:
    """Proper configs and show all log entries"""
    assert (request.node.name, logging.DEBUG, "debug_message") in log_fixture_0
    assert (request.node.name, logging.INFO, "info_message") in log_fixture_0
    assert (request.node.name, logging.WARNING, "warning_message") in log_fixture_0
    assert (request.node.name, logging.ERROR, "error_message") in log_fixture_0
    assert (request.node.name, logging.CRITICAL, "critical_message") in log_fixture_0


def test_case_5(log_fixture_0: list, request: SubRequest) -> None:
    """Non-set logger content, inherit full default"""
    assert (request.node.name, logging.DEBUG, "debug_message") not in log_fixture_0
    assert (request.node.name, logging.INFO, "info_message") in log_fixture_0
    assert (request.node.name, logging.WARNING, "warning_message") in log_fixture_0
    assert (request.node.name, logging.ERROR, "error_message") in log_fixture_0
    assert (request.node.name, logging.CRITICAL, "critical_message") in log_fixture_0


def test_case_6(log_fixture_0: list, request: SubRequest) -> None:
    """Proper configs and only > debug log entries"""
    assert (request.node.name, logging.DEBUG, "debug_message") not in log_fixture_0
    assert (request.node.name, logging.INFO, "info_message") in log_fixture_0
    assert (request.node.name, logging.WARNING, "warning_message") in log_fixture_0
    assert (request.node.name, logging.ERROR, "error_message") in log_fixture_0
    assert (request.node.name, logging.CRITICAL, "critical_message") in log_fixture_0


def test_case_7(log_fixture_0: list, request: SubRequest) -> None:
    """Proper configs and only > info entries"""
    assert (request.node.name, logging.DEBUG, "debug_message") not in log_fixture_0
    assert (request.node.name, logging.INFO, "info_message") not in log_fixture_0
    assert (request.node.name, logging.WARNING, "warning_message") in log_fixture_0
    assert (request.node.name, logging.ERROR, "error_message") in log_fixture_0
    assert (request.node.name, logging.CRITICAL, "critical_message") in log_fixture_0


def test_case_8(log_fixture_0: list, request: SubRequest) -> None:
    """Proper configs and only > warning entries"""
    assert (request.node.name, logging.DEBUG, "debug_message") not in log_fixture_0
    assert (request.node.name, logging.INFO, "info_message") not in log_fixture_0
    assert (request.node.name, logging.WARNING, "warning_message") not in log_fixture_0
    assert (request.node.name, logging.ERROR, "error_message") in log_fixture_0
    assert (request.node.name, logging.CRITICAL, "critical_message") in log_fixture_0


def test_case_9(log_fixture_0: list, request: SubRequest) -> None:
    """Proper configs and only > error entries"""
    assert (request.node.name, logging.DEBUG, "debug_message") not in log_fixture_0
    assert (request.node.name, logging.INFO, "info_message") not in log_fixture_0
    assert (request.node.name, logging.WARNING, "warning_message") not in log_fixture_0
    assert (request.node.name, logging.ERROR, "error_message") not in log_fixture_0
    assert (request.node.name, logging.CRITICAL, "critical_message") in log_fixture_0


def test_case_10(log_fixture_0: list, request: SubRequest) -> None:
    """Proper configs and disabled logging"""
    assert (request.node.name, logging.DEBUG, "debug_message") not in log_fixture_0
    assert (request.node.name, logging.INFO, "info_message") not in log_fixture_0
    assert (request.node.name, logging.WARNING, "warning_message") not in log_fixture_0
    assert (request.node.name, logging.ERROR, "error_message") not in log_fixture_0
    assert (request.node.name, logging.CRITICAL, "critical_message") not in log_fixture_0


def test_case_11() -> None:
    """Invalid configuration type for default"""
    with pytest.raises(module_0.ConfigurationError):
        module_1.application_logging({"default": "shouldbedict"})
    with pytest.raises(module_0.ConfigurationError):
        module_1.application_logging({"default": ["shouldbedict"]})


def test_case_12() -> None:
    """Faulty config type"""
    str_0 = "randomtext"
    with pytest.raises(module_0.ConfigurationError):
        module_1.application_logging(str_0)


def test_case_13() -> None:
    """Default config"""
    dict_0 = {"randomtext": {}, "default": {"console": {"level": 10}}}
    dict_1 = module_1._generate_default(dict_0)
    assert "file" in dict_1
