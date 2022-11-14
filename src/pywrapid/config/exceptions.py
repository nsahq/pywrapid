#!/usr/bin/python3
"""
Configuration exceptions

Generic coniguration exceptions to use as is or as a base for
your extended configuration management.

Configuration base exception:
ConfigurationError
"""
# __author__ = "Jonas Werme"
# __copyright__ = "Copyright (c) 2021 Jonas Werme"
# __credits__ = ["nsahq"]
# __license__ = "MIT"
# __version__ = "1.0.0"
# __maintainer__ = "Jonas Werme"
# __email__ = "jonas[dot]werme[at]hoofbite[dot]com"
# __status__ = "Prototype"


class ConfigurationException(Exception):
    """Base Configuration Exception"""


class ConfigurationError(ConfigurationException):
    """Configuration Error Exception"""


class ConfigurationValidationError(ConfigurationError):
    """Generic Configuration Error Exception"""


class ConfigurationFileNotFoundError(ConfigurationError):
    """Generic Configuration Error Exception"""
