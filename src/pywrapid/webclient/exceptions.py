#!/usr/bin/python3
"""
Client generic exceptions

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


# Client
class ClientException(Exception):
    """Base exception"""


class ClientAuthorizationError(ClientException):
    """Client Authorization Error Exception"""


class ClientAuthenticationError(ClientException):
    """Client Authorization Error Exception"""


class ClientTokenRefreshError(ClientException):
    """Token Refresh Error Exception"""


class ClientTimeout(ClientException):
    """Client Timeout Exception"""


class ClientConnectionError(ClientException):
    """Client Connection Error Exception"""


class ClientHTTPError(ClientException):
    """Client HTTP Error Exception"""


class ClientURLError(ClientException):
    """Client URL Error Exception"""


# Credentials
class CredentialError(Exception):
    """Credential Certificate Error Exception"""


class CredentialCertificateFileError(CredentialError):
    """Credential Certificate Error Exception"""


class CredentialKeyFileError(CredentialError):
    """Credential Key Error Exception"""


class CredentialURLError(CredentialError):
    """Credential URL Error Exception"""
