#!/usr/bin/python3
"""
Pywrapid generic exceptions

Generic pywrapid exceptions to use as is or as a base for
your extended functionality or base exception for error handling.

Pywrapid base exception:
PywrapidError

"""
# __author__ = "Jonas Werme"
# __copyright__ = "Copyright (c) 2021 Jonas Werme"
# __credits__ = ["nsahq"]
# __license__ = "MIT"
# __version__ = "1.0.0"
# __maintainer__ = "Jonas Werme"
# __email__ = "jonas[dot]werme[at]hoofbite[dot]com"
# __status__ = "Prototype"


class PywrapidException(Exception):
    """Base Pywrapid Exception"""


class PywrapidError(PywrapidException):
    """Base Pywrapid Error"""


class DependencyError(PywrapidError):
    """Dependency Error Exception"""
