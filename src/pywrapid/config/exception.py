#!/usr/bin/python3
"""
Configuration exceptions

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


class ConfigurationException(Exception):
    """Base exception"""


class ConfigurationError(ConfigurationException):
    """Generic Configuration Error Exception"""


class ConfigurationValidationError(ConfigurationException):
    """Generic Configuration Error Exception"""


class ConfigurationFileNotFoundError(ConfigurationException):
    """Generic Configuration Error Exception"""
