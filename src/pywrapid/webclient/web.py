#!/usr/bin/python3
"""
pywrapid web client base

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
# __version__ = "0.1.0"
# __maintainer__ = "Jonas Werme"
# __email__ = "jonas[dot]werme[at]hoofbite[dot]com"
# __status__ = "Prototype"


import logging
from datetime import datetime, timedelta
from enum import Enum
from time import time
from typing import Any, Type
from urllib.parse import urlparse

import jwt
from requests import HTTPError, RequestException, Response, Timeout, TooManyRedirects, request

from pywrapid.config.config import WrapidConfig
from pywrapid.utils.file_tools import is_file_readable

from .exceptions import (
    ClientAuthenticationError,
    ClientConnectionError,
    ClientException,
    ClientHTTPError,
    ClientTimeout,
    CredentialCertificateFileError,
    CredentialError,
    CredentialKeyFileError,
    CredentialURLError,
)

log = logging.Logger(__name__)


class AuthorizationType(Enum):
    """Auth type enum"""

    NONE = 0
    BASIC = 1
    BEARER = 2
    JWT = 3
    OAUTH2 = 4


# class Authorization():
#     """Base class for authorization"""

#     def __init__(self, auth_header="") -> None:
#         """Fix me"""
#         self.authorization_header = auth_header


# class BearerAuthorization(Authorization):
#     """Bearer auth is used in requests"""

#     def __init__(self, login_url: str = "") -> None:
#         """Fix me"""
#         super().__init__("Bearer")


# class BasicAuthorization(Authorization):
#     """Basic Auth is used in request"""

#     def __init__(self) -> None:
#         """Fix me"""
#         super().__init__("Basic")


class WebCredentials:
    """Credential base class"""

    def __init__(self, login_url: str = "") -> None:
        """Init class for web credentials"""
        if login_url and not urlparse(login_url):
            log.debug("Login URL validation failed for URL:  %s", login_url)
            raise CredentialURLError("Validation failed for login URL")
        self._login_url = login_url
        self._options: dict = {}

    @property
    def options(self) -> dict:
        """Getter for options"""
        return dict(self._options)

    @property
    def login_url(self) -> str:
        """Getter for login url"""
        return str(self._login_url)


class BasicAuthCredentials(WebCredentials):
    """Credential class for basic auth"""

    def __init__(self, username: str, password: str, login_url: str = "", wrapid_config: Type[WrapidConfig] = None) -> None:
        if wrapid_config and (login_url):
            raise CredentialError("Multiple configuration options used, use either a WrapidConfig derivative OR pass parameters")

        if wrapid_config:
            login_url = wrapid_config.cfg.get("login_url", "")

        super().__init__(login_url=login_url)

        self._options = {"auth": (username, password)}


class X509Credentials(WebCredentials):
    """Credential class for basic auth"""

    def __init__(self, cert_file: str = "", key_file: str = "", login_url: str = "", wrapid_config: Type[WrapidConfig] = None) -> None:

        if wrapid_config and (cert_file or key_file or login_url):
            raise CredentialError("Multiple configuration options used, use either a WrapidConfig derivative OR pass parameters")

        if wrapid_config:
            cert_file = wrapid_config.cfg.get("cert_file", "")
            key_file = wrapid_config.cfg.get("key_file", "")
            login_url = wrapid_config.cfg.get("login_url", "")

        super().__init__(login_url=login_url)

        if not is_file_readable(cert_file):
            raise CredentialCertificateFileError("Certificate file error")
        if not is_file_readable(key_file):
            raise CredentialKeyFileError("Key file error")

        self._options = {"cert": (cert_file, key_file)}


class WebClient:
    """Web Client

    Generic web client class as base for creating application specific clients
    or to be used directly as a general use web client. Wraps the request library and
    adds generic exceptions.

    Passes web calls transparently to requests, meaning you can use any requests
    option you see fit, such as proxy settings etc.

    The client allows you to mix and match authetication types with authorization
    types to fit strange combinations used in some APIs.

    Can be used with a wrapid config or straight up dict config for use in clients
    extending this class.

    Allows raise of exception on non-2xx responses (optional).
    """

    def __init__(
        self,
        authorization_type: AuthorizationType = AuthorizationType.NONE,
        credentials: Type[WebCredentials] = None,
        dict_config: dict = None,
        wrapid_config: Type[WrapidConfig] = None,
    ):
        """Init function for web client class

        Args:
            authorization_type (AuthorizationType (ENUM), optional):
                wrapid authorization type to use for clients communication.

            credentials (Type[WebCredentials], optional):
                wrapid credentials object to use for clients communication.

            dict_config (dict, optional, mutually exlusive with wrapid_conf):
                dict object to store in the clients config parameter.

            wrapid_config (Type[WrapidConfig], optional, mutually exlusive with dict_config):
                wrapid configuration object to store configuration in the clients
                config parameter from.

        Raises:
            ClientException
        """
        self._config = {}

        if wrapid_config and dict_config:
            raise ClientException(
                "Initiation error: dict_config and wrapid_config are mutually exclusive"
            )
        if wrapid_config:
            self._config = wrapid_config.cfg
        elif dict_config:
            self._config = dict_config

        self._authorization_type = authorization_type

        if credentials:
            self._credential_options = credentials.options()  # type: ignore
            self._login_url = credentials.login_url()  # type: ignore
        self._authorization_expiry = datetime.now()
        self._access_token = ""  # nosec

        log.debug(
            "Initiating new client with authorization type %s and credential type %s",
            AuthorizationType(authorization_type).name,
            type(credentials),
        )

    def _unpack_jwt(self, token: str) -> dict:
        """Decodes and unpacks JWT tokens content

        Does not include signature verification or encrypted parts

        Args:
            token (str): Token to unpack

        Returns:
            dict: _description_
        """
        # Following 4 lines can be simplified with token.removeprefix("Bearer ")
        # for python version > 3.9
        # Keeping for backwards compatibillity for now
        bearer = "Bearer "
        jwt_token = token

        if token.startswith(bearer):
            jwt_token = token[len(bearer) :]

        return jwt.decode(jwt_token, options={"verify_signature": False})

    def generate_session(self, method: str = "POST") -> None:
        """Authenticate and generate new token

        Args:
            method (str, optional): HTTP Method to use. Defaults to "POST".

        Raises:
            ClientAuthenticationError
        """

        response = self.call(
            method=method,
            url=self._login_url,
            raise_for_status=True,
            skip_authentication=True,
        )

        if response.status_code > 299 or response.status_code < 200:
            log.debug(
                "Failed login: [%s] %s @ %s",
                response.status_code,
                response.content,
                self._login_url,
            )
            raise ClientAuthenticationError(
                f"Login attempt failed: [{response.status_code}] {response.content!r}"
            )

        if "Authorization" in response.headers:
            self._access_token = response.headers["Authorization"]

        if self._authorization_type == AuthorizationType.JWT:
            unix_now = time()
            jwt_data = self._unpack_jwt(self._access_token)
            log.debug("JWT data: %s", jwt_data)

            for exp in ["expiresIn", "exp", "expires_in", "expires"]:
                if exp in jwt_data:
                    if jwt_data[exp] < 44640:
                        self._authorization_expiry = datetime.fromtimestamp(
                            unix_now + jwt_data[exp]
                        )
                    else:
                        self._authorization_expiry = datetime.fromtimestamp(jwt_data[exp])
            log.debug("Authorization expiry time set to: %s", self._authorization_expiry)

    def call(
        self,
        method: str,
        url: str,
        raise_for_status: bool = False,
        skip_authentication: bool = False,
        **options: Any,
    ) -> Response:
        """Send web request to the target url

        Args:
            method (str): Method of the HTTP request
            url (str): URL of the request
            raise_for_status (bool): Raise for non 2xx repsonses
            skip_authentication (bool): Skip authentication and skip token refresh controls
            **options (dict): request options

        Raises:
            ClientHTTPError
            ClientTimeout
            ClientConnectionError
            ClientException
            ClientAuthenticationError

        Returns:
            Response: requests.Response object
        """
        # Handle authentication and token refresh
        time_offset = datetime.now() + timedelta(seconds=1)  # Offset to avoid ms/ns race condition
        if (
            self._login_url and not self._access_token
        ) or self._authorization_expiry < time_offset:
            if not skip_authentication:
                self.generate_session()

        if "cert" not in options and "auth" not in options:
            options = {**options, **self._credential_options}

        if "Authorization" not in options and self._authorization_type != AuthorizationType.NONE:
            options["header"]["Authorization"] = self._access_token

        try:
            response = request(method, url, **options)

            if raise_for_status:
                response.raise_for_status()

        except HTTPError as error:
            raise ClientHTTPError from error
        except Timeout as error:
            raise ClientTimeout from error
        except TooManyRedirects as error:
            raise ClientConnectionError from error
        except RequestException as error:
            raise ClientException from error

        return response
