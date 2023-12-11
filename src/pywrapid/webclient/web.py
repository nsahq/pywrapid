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
from typing import Any, Optional, Type, Union
from urllib.parse import urlparse

import jwt
from requests import HTTPError, RequestException, Response, Timeout, TooManyRedirects, request

from pywrapid.config import ConfigSubSection, WrapidConfig
from pywrapid.utils import is_file_readable

from .exceptions import (
    ClientAuthenticationError,
    ClientAuthorizationError,
    ClientConnectionError,
    ClientError,
    ClientHTTPError,
    ClientTimeout,
    CredentialCertificateFileError,
    CredentialError,
    CredentialKeyFileError,
    CredentialURLError,
)

log = logging.getLogger(__name__)


class AuthorizationType(Enum):
    """Auth type enum"""

    NONE = 0
    BASIC = 1
    BEARER = 2
    JWT = 3
    OAUTH2 = 4


class WebCredentials:
    """Credential base class"""

    def __init__(self) -> None:
        """Init class for web credentials"""
        self._options: dict = {}
        self._config: dict = {}
        self.type = type(self).__name__

    @property
    def options(self) -> dict:
        """Getter for options"""
        return self._options

    @property
    def config(self) -> dict:
        """Getter for options"""
        return self._config

    def _unify_configuration(
        self, params: dict, config: Union[Type[WrapidConfig], dict, None]
    ) -> ConfigSubSection:
        """Unify params and config values

        Produces wrapid config (ConfigSubSection) object after validating standard stuff.

        Args:
            params (dict): Configuration parameters, e.g. locals()
            config (WrapidConfig|dict): Configuration object, dict or None
        """
        params = {
            k: v
            for k, v in params.items()
            if k != "self" and k != "kwargs" and k != "config" and k != "__class__" and v
        }

        if params and config:
            raise CredentialError(
                "Multiple configuration options used, "
                "use a WrapidConfig derivative/dict OR passed parameters"
            )

        if params:
            config = params

        if isinstance(config, dict):
            config = ConfigSubSection({"dummy_key": config}, "dummy_key")  # type: ignore

        if config and isinstance(config, WrapidConfig):
            return config

        raise CredentialError(
            "Config pratameter must be of type dict or a WrapidConfig derivative"
        )

    # def import_dependencies(self, dependencies: list) -> bool:
    #     """Import dependencies for credential type"""
    #     missing_dependencies = []
    #     for dependency in dependencies:
    #         if not is_module_available(dependency):
    #             log.error("Dependency %s is not available", dependency)
    #             missing_dependencies.append(dependency)
    #             continue
    #         if not is_module_already_imported(dependency):
    #             setattr(self, dependency, import_module(dependency))

    #     if missing_dependencies:
    #         raise DependencyError(f"Missing credential dependencies: {missing_dependencies}")

    #     log.debug("All credential dependencies (%s) are available", dependencies)

    #     return True

    def validate_url(self, url: str = "", raise_on_fail: bool = False) -> bool:
        """Validate URL strings

        Args:
            url (str, optional): The URL to validate. Defaults to "".
            raise_on_fail (bool, optional): Raise error if validation fails. Defaults to False.

        Raises:
            CredentialURLError: _description_

        Returns:
            bool: _description_
        """
        if not url or not urlparse(url):
            log.error("URL validation failed for URL:  %s", self._config[url])
            if raise_on_fail:
                raise CredentialURLError("Validation failed for URL")
            return False

        return True


class BasicAuthCredentials(WebCredentials):
    """Credential class for basic auth"""

    def __init__(  # pylint: disable=unused-argument
        self,
        username: str,
        password: str,
        login_url: str = "",
        config: Union[Type[WrapidConfig], dict, None] = None,
        **kwargs: dict[str, Any],
    ) -> None:
        wrapid_config = self._unify_configuration({**locals(), **kwargs}, config)  # type: ignore
        super().__init__()

        required_keys = ["username", "password"]

        wrapid_config.validate_keys(expected_keys=required_keys)  # type: ignore
        self._config = dict(wrapid_config.cfg)

        if "login_url" in self._config:
            self.validate_url(str(self._config.get("login_url")))

        self._options = {"auth": (username, password)}


class X509Credentials(WebCredentials):
    """Credential class for x509 auth"""

    def __init__(  # pylint: disable=unused-argument, too-many-arguments
        self,
        cert_file: str = "",
        key_file: str = "",
        login_url: str = "",
        jwt_key: str = "",
        access_token_timeout: int = 0,
        token_expiry_offset: int = 0,
        config: Union[Type[WrapidConfig], dict, None] = None,
        **kwargs: dict[str, Any],
    ) -> None:
        wrapid_config = self._unify_configuration({**locals(), **kwargs}, config)
        super().__init__()

        required_keys = ["login_url", "key_file", "cert_file"]
        wrapid_config.validate_keys(required_keys)

        self._config = dict(wrapid_config.cfg)

        self.cert_file = self._config.get("cert_file", "")
        self.key_file = self._config.get("key_file", "")
        self.login_url = self._config.get("login_url", "")

        if not is_file_readable(self.cert_file):
            log.error("Certificate file validation failed for %s", self.cert_file)
            raise CredentialCertificateFileError("Certificate file error")
        if not is_file_readable(self.key_file):
            log.error("Key file validation failed for %s", self.key_file)
            raise CredentialKeyFileError("Key file error")

        log.debug(
            "Loading x509 web credentials: cert_file=%s, key_file=%s, login_url=%s",
            self.cert_file,
            self.key_file,
            self.login_url,
        )

        self._options = {"cert": (self.cert_file, self.key_file)}


class OAuth2Credentials(WebCredentials):
    """Credential class for OAauth2 authentication"""

    def __init__(  # pylint: disable=unused-argument, too-many-arguments  # nosec
        self,
        login_url: str = "",
        token_url: str = "",
        redirect_uri: str = "",
        auth_data: dict | None = None,
        legacy_auth: BasicAuthCredentials | None = None,
        refresh_token_timeout: int = 0,
        access_token_timeout: int = 0,
        token_expiry_offset: int = 0,
        config: Union[Type[WrapidConfig], dict, None] = None,
        **kwargs: dict[str, Any],
    ) -> None:
        # self.import_dependencies(["requests_oauthlib"])
        wrapid_config = self._unify_configuration({**locals(), **kwargs}, config)
        super().__init__()

        required_keys = ["login_url", "auth_data"]

        self._config = dict(wrapid_config.cfg)

        for url in ["login_url", "token_url", "redirect_uri"]:
            use_url = ""
            if url in self._config:
                self.validate_url(url)
                use_url = str(self._config.get(url))
                if url not in required_keys:
                    required_keys.append(url)
            setattr(self, url, use_url)

        wrapid_config.validate_keys(required_keys)

        self.legacy_auth = self._config.get("legacy_auth", None)

        log.debug(
            "Loading OAuth2 web credentials: login_url=%s, "
            "token_url=%s, redirect_uri=%s, legacy_auth=%s",
            self.login_url,  # type: ignore # pylint: disable=no-member
            self.token_url,  # type: ignore # pylint: disable=no-member
            self.redirect_uri,  # type: ignore # pylint: disable=no-member
            bool(self.legacy_auth),
        )

        if legacy_auth:
            self._options = self._config["legacy_auth"]._options

        self.credential_body = self._config.pop("auth_data")


class WebClient:  # pylint: disable=too-many-instance-attributes, too-many-arguments
    """Web Client base

    Generic web client class as base for creating application specific clients
    or to be used directly as a general use web client. Wraps the request library and
    adds generic exceptions.

    Passes web calls transparently to requests, meaning you can use any requests
    option you see fit, such as proxy settings etc by passing them as key word arguments.
    If a configuration section named client_options is passed to the client,
    these options will be set for the web communication. Passed arguments will have precedence
    over configuration items.

    The client allows you to mix and match authetication types with authorization
    types to fit strange combinations used in some APIs.

    Can be used with a wrapid config or straight up dict config for use in clients
    extending this class.

    Allows raise of exception on non-2xx responses (optional).
    """

    def __init__(
        self,
        authorization_type: AuthorizationType = AuthorizationType.NONE,
        credentials: Optional[Type[WebCredentials]] = None,
        dict_config: Optional[dict] = None,
        wrapid_config: Optional[Type[WrapidConfig]] = None,
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
            raise ClientError(
                "Initiation error: dict_config and wrapid_config are mutually exclusive"
            )
        if wrapid_config:
            self._config = wrapid_config.cfg
        elif dict_config:
            self._config = dict_config

        self._authorization_type = authorization_type

        if credentials:
            self._credential_options: dict = {**credentials.options}  # type: ignore[dict-item]
            self._login_url = credentials.config.get("login_url", "")  # type: ignore[attr-defined]
            self._credential_config = credentials.config
            if isinstance(credentials, OAuth2Credentials):
                self._credential_body: dict = credentials.credential_body
            else:
                self._credential_body = {}
        self._access_token_expiry = datetime.now()
        self._refresh_token_expiry = datetime.now()
        self._access_token = ""  # nosec
        self._refresh_token = ""  # nosec

        try:
            AuthorizationType(authorization_type).name
        except ValueError as error:
            raise ClientAuthorizationError(error) from error
        log.debug(
            "Initiating new client with authorization type %s and credential type %s",
            AuthorizationType(authorization_type).name,
            type(credentials).__name__,
        )

    def _unpack_jwt(self, token: str) -> dict:
        """Decodes and unpacks JWT tokens content

        Does not include signature verification or encrypted parts

        Args:
            token (str): Token to unpack

        Returns:
            dict: Unpacked JWT token
        """
        additionals = {}
        if self._credential_options.get("jwt_secret", None):
            additionals["key"] = self._config["jwt_secret"]
        if self._credential_options.get("jwt_algorithms", None):
            additionals["algorithms"] = self._credential_options.get("jwt_algorithms")

        return jwt.decode(token, options={"verify_signature": False}, **additionals)

    def session_expired(self) -> bool:
        """Check if our session has expired

        Returns:
            bool: True if token is expired, False if still valid
        """
        if not self._access_token_expiry or not self._access_token:
            return True

        time_offset = datetime.now() + timedelta(
            seconds=self._config.get("token_expiry_offset", 10)
        )  # Offset to avoid ms/ns race condition
        if time_offset < self._access_token_expiry:
            return False

        return True

    def generate_session(self, method: str = "POST", **options: Any) -> None:
        """Authenticate and generate new token

        Args:
            method (str, optional): HTTP Method to use. Defaults to "POST".

        Raises:
            ClientAuthenticationError
        """
        if self._credential_body:
            options["data"] = self._credential_body

        response = self.call(
            method,
            str(self._login_url),
            raise_for_status=False,
            skip_authentication=True,
            **options,
        )

        if response.status_code > 299 or response.status_code < 200:
            log.error(
                "Unable to generate new session: [%s] %s @ %s",
                response.status_code,
                response.content,
                self._login_url,
            )
            raise ClientAuthenticationError(
                f"Unable to generate new session: [{response.status_code}] {response.content!r}"
            )

        self._parse_authentication_data(response)

    def _parse_authentication_data(  # pylint: disable=too-many-branches
        self, response: Response
    ) -> None:
        # Custom headers or custom bodies are common locations of bearer tokens.
        # We need to make this more dynamic later. Adding response Authorization header
        # and a few more for now
        # Typically used for custom x509 auth but also common for basic auth and custom
        # implementations
        if "Authorization" in response.headers:
            self._set_access_token(response.headers["Authorization"])

        # Custom configured header
        if self._config.get("access_token_header", ""):
            if self._config["access_token_header"] in response.headers:
                self._set_access_token(response.headers[self._config["access_token_header"]])
            else:
                log.error(
                    "Unable to find access token header %s in response headers: %s",
                    self._config["access_token_header"],
                    response.headers,
                )
                raise ClientAuthenticationError("Unable to find configured access token header")

        # Manage JWT data extraction
        if self._authorization_type == AuthorizationType.OAUTH2:
            try:
                auth_response_data = response.json()
                # Oauth2 implementations differ vastly. Some gives only access_tokens,
                # some give both at authentication, some give both at every refresh
                # some give only refresh_tokens for offline scopes. Spliting ifs to handle all.
                if "access_token" in auth_response_data:
                    self._set_access_token(auth_response_data["access_token"])
                    if self._config.get("access_token_timeout", 0) == 0:
                        expiry = time() + auth_response_data.get("expires_in")
                    else:
                        expiry = time() + self._config.get("access_token_timeout", 0)

                    self._set_access_token_expiry(expiry)

                if "refresh_token" in auth_response_data:
                    self._set_refresh_token(auth_response_data["refresh_token"])
                    expiry = time() + self._config.get("refresh_token_timeout", 84600)
                    self._set_refresh_token_expiry(expiry)

            except ValueError as error:
                raise ClientAuthenticationError(error) from error
            except Exception as error:
                raise ClientAuthenticationError(error) from error

        if self._authorization_type in [
            AuthorizationType.JWT,
            AuthorizationType.BEARER,
        ]:
            self._set_access_token_expiry(self._get_jwt_expiry(self._access_token))
            if self._access_token_expiry < datetime.now():
                raise ClientAuthorizationError("JWT Access token expired or could not be set")

    def _get_jwt_expiry(self, token: str) -> float:
        """Get JWT token expiry time

        Args:
            token (str): JWT token

        Returns:
            float: Expiry time as unix timestamp
        """
        jwt_data = self._unpack_jwt(token)
        log.debug("JWT data: %s", jwt_data)
        expiry = time()

        for exp in ["exp", "expiresIn", "expires_in", "expires"]:  # standard = exp
            if exp in jwt_data:
                if jwt_data[exp] < 44640:  # Handle poor expiry implementations with offset
                    expiry = expiry + jwt_data[exp]
                else:
                    expiry = jwt_data[exp]
                break

        return expiry

    # flake8: noqa: C901
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
        if not skip_authentication and self.session_expired():
            self.generate_session(**self._credential_options)

        if self._access_token and self._authorization_type != AuthorizationType.NONE:
            if "headers" not in options:
                options["headers"] = {"Authorization": f"Bearer {self._access_token}"}
            else:
                if "Authorization" not in options["headers"]:
                    options["headers"] = {
                        "Authorization": f"Bearer {self._access_token}",
                        **options["headers"],
                    }
        if "client_options" in self.get_config:
            options = {**self.get_config["client_options"], **options}
        try:
            response = request(method, url, **options)

            if raise_for_status:
                response.raise_for_status()
        except HTTPError as error:
            raise ClientHTTPError(error) from error
        except Timeout as error:
            raise ClientTimeout(error) from error
        except TooManyRedirects as error:
            raise ClientConnectionError(error) from error
        except RequestException as error:
            raise ClientError(error) from error

        return response

    @property
    def get_config(self) -> dict:
        """Get current configuration

        Returns:
            configuration {dict}  -- Dict representation of configuration"""
        return self._config

    def _set_refresh_token(self, refresh_token: str) -> None:
        """Set refresh token"""
        self._refresh_token = refresh_token

        log.debug("Refresh token set to: %s", self._refresh_token)

    def _set_refresh_token_expiry(self, refresh_expiry: float) -> None:
        """Set refresh token expiry time"""
        self._refresh_token_expiry = datetime.fromtimestamp(refresh_expiry)

        log.debug("Refresh token expiry set to: %s", self._refresh_token_expiry)

    def _set_access_token(self, access_token: str) -> None:
        """Set access token"""
        # Following 4 lines can be simplified with token.removeprefix("Bearer ")
        # for python version > 3.9
        # Keeping for backwards compatibillity for now
        bearer = "Bearer "

        if access_token.startswith(bearer):
            access_token = access_token[len(bearer) :]

        self._access_token = access_token

        log.debug("Access token set to: %s", self._access_token)

    def _set_access_token_expiry(self, access_expiry: float) -> None:
        """Set access token expiry time"""
        self._access_token_expiry = datetime.fromtimestamp(access_expiry)

        log.debug("Access token expiry set to: %s", self._access_token_expiry)
