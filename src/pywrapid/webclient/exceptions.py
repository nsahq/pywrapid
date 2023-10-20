#!/usr/bin/python3
"""
Client generic exceptions

Generic client and credential exceptions to use as is or as a base for
your extended client/credential management.

Client base exception:
ClientError

Credential base exception:
CredentialError

"""
# __author__ = "Jonas Werme"
# __copyright__ = "Copyright (c) 2021 Jonas Werme"
# __credits__ = ["nsahq"]
# __license__ = "MIT"
# __version__ = "1.0.0"
# __maintainer__ = "Jonas Werme"
# __email__ = "jonas[dot]werme[at]hoofbite[dot]com"
# __status__ = "Prototype"

from pywrapid.utils.exceptions import PywrapidError, PywrapidException


# Client
class ClientException(PywrapidException):
    """Base Client Exception"""


class ClientError(PywrapidError):
    """Client Error Exception"""


class ClientAuthorizationError(ClientError):
    """Client Authorization Error Exception"""


class ClientAuthenticationError(ClientError):
    """Client Authorization Error Exception"""


class ClientTokenRefreshError(ClientError):
    """Token Refresh Error Exception"""


class ClientTimeout(ClientError):
    """Client Timeout Exception"""


class ClientConnectionError(ClientError):
    """Client Connection Error Exception"""


class ClientHTTPError(ClientError):
    """Client HTTP Error Exception"""


class ClientURLError(ClientError):
    """Client URL Error Exception"""


# Credentials
class CredentialException(PywrapidException):
    """Credential Certificate Error Exception"""


class CredentialError(PywrapidError):
    """Credential Certificate Error Exception"""


class CredentialCertificateFileError(CredentialError):
    """Credential Certificate Error Exception"""


class CredentialKeyFileError(CredentialError):
    """Credential Key Error Exception"""


class CredentialURLError(CredentialError):
    """Credential URL Error Exception"""
