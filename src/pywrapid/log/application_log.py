#!/usr/bin/python3
"""
Log manager for easy and fast log compliancy

This library is for educational purposes only.
Do no evil, do not break local or internation laws!
By using this code, you take full responisbillity for your actions.
The author have granted code access for educational purposes and is
not liable for any missuse.
"""
__author__ = "Jonas Werme"
__copyright__ = "Copyright (c) 2021 Jonas Werme"
__credits__ = ["Marcus Wallgren", "nsahq"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jonas Werme"
__email__ = "jonas[dot]werme[at]nsahq[dot]se"
__status__ = "Prototype"

import logging
from logging.handlers import SysLogHandler
from typing import Type, Union

from pywrapid.config import WrapidConfig
from pywrapid.config.exceptions import ConfigurationError
from pywrapid.utils import dict_merge


def _generate_default(cfg: dict) -> dict:
    """Generate default config dict for logging

    Args:
        cfg (dict): Logging configuration

    Raises:
        ConfigurationError

    Returns:
        dict: Default logging configuration
    """
    if not isinstance(cfg, dict):
        raise ConfigurationError("Invalid application logging configuration type")

    default = {
        "console": {
            "format": "[%(levelname)s] (%(name)s) %(message)s",
            "level": logging.INFO,
        },
        "file": {
            "format": "%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s",
            "level": logging.INFO,
            "location": "",
        },
        "syslog": {
            "format": "%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s",
            "level": 0,
            "location": "/dev/log",
            "ident": "pywrapid-default-ident",
        },
    }

    if not cfg:
        return default

    if "default" in cfg and cfg["default"]:
        if not isinstance(cfg["default"], dict):
            raise ConfigurationError("Invalid object in configuration section: default")
        default = dict_merge(default, cfg["default"])

    return default


# flake8: noqa: C901
def application_logging(  # pylint: disable=too-many-branches
    config: Union[Type[WrapidConfig], dict]
) -> None:
    """Sets up loggers for application

    Configuration used for setting up all specified loggers
    as well as the root logger.

    Args:
        config (WrapidConfig|dict): Wrapid config object or dict of modules and options

    """
    if isinstance(config, WrapidConfig):
        cfg = config.cfg
    elif isinstance(config, dict):
        cfg = config
    else:
        raise ConfigurationError("Invalid application logging configuration type")

    logging.root.setLevel(logging.NOTSET)

    default = _generate_default(cfg=cfg)

    cfg["root"] = default
    for module in cfg:
        if module == "default":
            continue

        log = logging.getLogger(module) if module != "root" else logging.getLogger()

        log.propagate = False
        # if log.hasHandlers():
        #     continue
        cfg[module] = dict_merge(default, cfg[module]) if cfg[module] is not None else default
        for log_type in ["console", "file", "syslog"]:
            formatter = logging.Formatter(cfg[module].get("format", default[log_type]["format"]))
            level = cfg[module][log_type].get("level", default[log_type]["level"])

            if level == 0:
                continue

            if log_type == "console":
                handler: logging.Handler = logging.StreamHandler()
            elif log_type == "file":
                if not cfg[module][log_type]["location"]:
                    continue
                handler = logging.FileHandler(
                    cfg[module].get("location", default[log_type]["location"])
                )
            elif log_type == "syslog":
                handler = SysLogHandler(
                    facility=SysLogHandler.LOG_DAEMON,
                    address=cfg[module].get("location", default[log_type]["location"]),
                )
                ident = cfg[module].get("ident", default[log_type]["ident"])

                if ident:
                    handler.ident = ident

            handler.setLevel(level)
            handler.setFormatter(formatter)
            log.addHandler(handler)
            if log.getEffectiveLevel() > level:
                log.setLevel(level)
            if log.getEffectiveLevel() == 0:
                log.setLevel(10)
            # if log.root.getEffectiveLevel() > level:
            #     log.root.setLevel(level)
