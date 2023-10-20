#!/usr/bin/python3
"""
Config manager for easy and fast configuration functionality

This library is for educational purposes only.
Do no evil, do not break local or internation laws!
By using this code, you take full responisbillity for your actions.
The author have granted code access for educational purposes and is
not liable for any missuse.
"""
# __author__ = "Jonas Werme"
# __copyright__ = "Copyright (c) 2021 Jonas Werme"
# __credits__ = ["nsahq"]
# __license__ = "MIT"
# __version__ = "1.0.0"
# __maintainer__ = "Jonas Werme"
# __email__ = "jonas[dot]werme[at]hoofbite[dot]com"
# __status__ = "Prototype"

import logging
import os
from typing import Optional, Type, Union

import yaml

from pywrapid.config.exceptions import (
    ConfigurationError,
    ConfigurationFileNotFoundError,
    ConfigurationValidationError,
)
from pywrapid.utils import dict_keys_exist, is_file_readable

log = logging.getLogger(__name__)


class WrapidConfig:
    """Base configuration class"""

    cfg: dict = {}

    def validate_keys(self, expected_keys: list, allow_empty: bool = False) -> bool:
        """Validate keys in configuration

        Args:
            expected_keys (list): _description_
            allow_empty (bool, optional): _description_. Defaults to False.

        Raises:
            ConfigurationValidationError

        Returns:
            bool: Validation status. Keys exist in top level.
        """

        if not self.cfg:
            raise ConfigurationError("No configuration has been set")
        log.debug("Making sure %s is present in config top level", expected_keys)

        try:
            return dict_keys_exist(
                data=self.cfg,
                expected_keys=expected_keys,
                allow_empty=allow_empty,
                raise_on_fail=True,
            )
        except ValueError as error:
            raise ConfigurationValidationError(
                f"Configuration content did not pass validation: {error}"
            ) from error

    def is_file_usable(self, path: str) -> bool:
        """Check if file is present, accessible and readable

        Args:
            path (str): Path to configuration file.

        Returns:
            bool: Indicating validation success.
        """
        log.debug("Validating if path %s is an accessible file", path)
        return is_file_readable(path)

    def application_config_location(
        self, application_name: str, file_type: str = "yml", locations: Optional[list] = None
    ) -> str:
        """Discovery to find configuration file for an application on Windows/Linux/Mac

        Uses a set list of default/common configration locations

        Config precedence:
        1.  Locations parameter:        [parameter,provided,list,of,locations]
        2.  Environment variable:       APPLICATION_NAME_CONFIG_PATH
        3.  Relative path:              application_name.type
        4.  Relative path:              config.type
        3.  Configuration location:     %APPDATA%/application_name/application_name.type
        4.  Configuration location:     %APPDATA%/application_name/config.type
        5.  Configuration location:     $XDG_CONFIG_HOME/application_name/application_name.type
        6.  Configuration location:     $HOME/.application_name
        7.  Configuration location:     $HOME/.config/application_name.type
        8.  Configuration location:     /etc/application_name"
        9.  Configuration location:     /etc/application_name.type"
        10. Configuration location:     /etc/application_name/application_name.type"
        11. Configuration location:     /etc/application_name/config.type"
        12. Configuration location:     /etc/application_name/config"
        13. Configuration location:     /etc/defaults/application_name"

        Args:
            application_name (str): The name of the application
            file_type (str, optional): The type of config file to find.
            locations (list, optional): List of paths to look in before discovery.

        Raises:
            ConfigurationFileNotFoundError

        Returns:
            str: Absolute path of the configuration file
        """

        config_file_name = f"{application_name}.{file_type}"

        if not locations:
            locations = []

        locations.extend(
            [
                os.environ.get(f"{application_name.upper()}_CONFIG_PATH"),
                config_file_name,
                f"config.{file_type}",
                f"{os.environ.get('APPDATA')}/{application_name}/{config_file_name}"
                if os.environ.get("APPDATA")
                else None,
                f"{os.environ.get('APPDATA')}/{application_name}/config.{file_type}"
                if os.environ.get("APPDATA")
                else None,
                f"{os.environ.get('XDG_CONFIG_HOME')}/{application_name}/{config_file_name}"
                if os.environ.get("XDG_CONFIG_HOME")
                else None,
                f"{os.environ.get('HOME')}/.{application_name}"
                if os.environ.get("HOME")
                else None,
                f"{os.environ.get('HOME')}/.config/{config_file_name}"
                if os.environ.get("HOME")
                else None,
                f"/etc/{application_name}",
                f"/etc/{config_file_name}",
                f"/etc/{application_name}/{config_file_name}",
                f"/etc/{application_name}/config.{file_type}",
                f"/etc/{application_name}/config",
                f"/etc/defaults/{application_name}",
            ]
        )

        for location in locations:
            if not location:
                continue

            p_loc = os.path.abspath(str(location))
            if is_file_readable(p_loc):
                return str(p_loc)

        raise ConfigurationFileNotFoundError("Unable to locate configuration file location")


class ApplicationConfig(WrapidConfig):
    """Application Configuration Class"""

    def __init__(
        self,
        application_name: str = "",
        config_path: str = "",
        file_type: str = "yml",
        allow_config_discovery: bool = False,
    ) -> None:
        """Init of ApplicationConfig
        Loads configuration from file

        Args:
            application_name (str, optional): Name of application.
            config_path (str, optional): Path to config file.
            file_type (str, optional): Config file type. Defaults to "yml".
            allow_config_discovery (bool, optional): Use exploration for config.
        """
        self.config_path: str = ""
        self.cfg: dict = {}

        if allow_config_discovery:
            self.config_path = self.application_config_location(
                application_name=application_name,
                file_type=file_type,
                locations=[config_path],
            )
        else:
            self.config_path = config_path

        if file_type.lower() in ["yml", "yaml"]:
            self.cfg = self.yaml_config_to_dict(self.config_path)

        # TODO: Add ini file

        # TODO: Add toml file

    def yaml_config_to_dict(
        self, config: str = "", expected_keys: Optional[list] = None, allow_empty: bool = False
    ) -> dict:
        """Extract configuration data from a yaml file

        Allows validation of key presence and value precence before returning
        the data set as a dict.

        Args:
            config (str, optional): Absolute or relative file path.
            expected_keys (list, optional): Keys which must exist in the data set.
            allow_empty (bool, optional): Allow keys with empty values.

        Raises:
            ConfigurationFileNotFoundError: _description_
            ConfigurationError: _description_

        Raises:
            ConfigurationFileNotFoundError: File is not present or inaccessible
            ValueError: Value in configuration file did not pass validation
            ConfigurationError: All other errors

        Returns:
            dict: Configuration settings
        """
        if not is_file_readable(config):
            raise ConfigurationFileNotFoundError(
                f"Readable configuration file not found: {config}"
            )

        if not expected_keys:
            expected_keys = []

        self.config_path = config

        try:
            with open(config, "r", encoding="utf-8-sig") as file:
                cfg = yaml.safe_load(file)
            if not isinstance(cfg, dict):
                raise ConfigurationValidationError(f"YAML parsing error for {config}")
            if expected_keys != []:
                self.validate_keys(expected_keys, allow_empty)

        except ConfigurationValidationError as error:
            raise ConfigurationValidationError(f"Loading of config failed: {error}") from error

        return cfg


class ConfigSubSection(WrapidConfig):
    """Configuration Subsection Class

    Sectioned configuration data from WrapidConfig object
    """

    def __init__(self, conf: Union[Type[WrapidConfig], dict], subsection: str = ""):
        """Init method of ConfigSubSection

        Args:
            conf (Type[WrapidConfig]): Derived object of WrapidConfig class
            subsection (str, optional): Key to extract configration from.

        Raises:
            ConfigurationError
        """
        if subsection == "":
            raise ConfigurationError("No configuration subsection specified")
        self._subsection_key = subsection

        if isinstance(conf, WrapidConfig):
            if subsection not in conf.cfg:
                raise ConfigurationError(f"Missing configuration section: {subsection}")
            self.cfg = conf.cfg[subsection].copy()
        elif isinstance(conf, dict):
            if subsection not in conf:
                raise ConfigurationError(f"Missing configuration section: {subsection}")
            self.cfg = conf[subsection].copy()
        else:
            raise ConfigurationError(f"Invalid object type for configuration, {type(conf)}")
