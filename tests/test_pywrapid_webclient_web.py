#!/usr/bin/python3
"""Pywrapid webclient tests"""

import locale as module_3
import os

import pytest

import pywrapid.config.exceptions as module_2
import pywrapid.webclient.exceptions as module_1
import pywrapid.webclient.web as module_0

# flake8: ignore=F841
# pylint: disable=protected-access


def test_case_0() -> None:
    """Built ins"""
    web_credentials_0 = module_0.WebCredentials()
    assert (
        f"{type(web_credentials_0).__module__}.{type(web_credentials_0).__qualname__}"
        == "pywrapid.webclient.web.WebCredentials"
    )
    assert (
        f"{type(module_0.WebCredentials.options).__module__}."
        f"{type(module_0.WebCredentials.options).__qualname__}" == "builtins.property"
    )


def test_case_1() -> None:
    """Built ins"""
    web_credentials_0 = module_0.WebCredentials()
    assert (
        f"{type(web_credentials_0).__module__}."
        f"{type(web_credentials_0).__qualname__}" == "pywrapid.webclient.web.WebCredentials"
    )
    assert (
        f"{type(module_0.WebCredentials.options).__module__}."
        f"{type(module_0.WebCredentials.options).__qualname__}" == "builtins.property"
    )


def test_case_2() -> None:
    """Empty param strings"""
    str_0 = ""
    with pytest.raises(module_1.CredentialError):
        module_0.X509Credentials(str_0, str_0, str_0)


def test_case_3() -> None:
    """WebClient type"""
    web_client_0 = module_0.WebClient()
    assert (
        f"{type(web_client_0).__module__}.{type(web_client_0).__qualname__}"
        == "pywrapid.webclient.web.WebClient"
    )


def test_case_4() -> None:
    """Random param strings"""
    str_0 = "agagjnqt"
    with pytest.raises(module_1.CredentialCertificateFileError):
        module_0.X509Credentials(str_0, str_0, str_0)


def test_case_5() -> None:
    """Basic Auth credentials for client"""
    str_0 = "#\nM,k(0Lf9E2-#Px9o\x0b*"
    basic_auth_credentials_0 = module_0.BasicAuthCredentials(str_0, str_0)
    assert (
        f"{type(basic_auth_credentials_0).__module__}.{type(basic_auth_credentials_0).__qualname__}"
        == "pywrapid.webclient.web.BasicAuthCredentials"
    )


def test_case_6() -> None:
    """Basic credentials for client"""
    web_client_0 = module_0.WebClient(dict_config={})
    assert (
        f"{type(web_client_0).__module__}.{type(web_client_0).__qualname__}"
        == "pywrapid.webclient.web.WebClient"
    )
    web_credentials_0 = module_0.WebCredentials()
    assert (
        f"{type(web_credentials_0).__module__}.{type(web_credentials_0).__qualname__}"
        == "pywrapid.webclient.web.WebCredentials"
    )
    assert (
        f"{type(module_0.WebCredentials.options).__module__}."
        f"{type(module_0.WebCredentials.options).__qualname__}" == "builtins.property"
    )

    web_credentials_1 = module_0.WebCredentials()
    module_0.WebClient(credentials=web_credentials_1, dict_config={})


def test_case_7() -> None:
    """Authorization type None for client"""
    authorization_type_0 = module_0.AuthorizationType.NONE
    web_client_0 = module_0.WebClient(authorization_type=authorization_type_0)
    assert (
        f"{type(web_client_0).__module__}.{type(web_client_0).__qualname__}"
        == "pywrapid.webclient.web.WebClient"
    )
    assert web_client_0._authorization_type == authorization_type_0


def test_case_8() -> None:
    """Authorization type Bearer for client"""
    authorization_type_0 = module_0.AuthorizationType.BEARER
    web_client_0 = module_0.WebClient(authorization_type=authorization_type_0)
    assert (
        f"{type(web_client_0).__module__}.{type(web_client_0).__qualname__}"
        == "pywrapid.webclient.web.WebClient"
    )
    assert web_client_0._authorization_type == authorization_type_0


def test_case_9() -> None:
    """Authorization type Basic for client"""
    authorization_type_0 = module_0.AuthorizationType.BASIC
    web_client_0 = module_0.WebClient(authorization_type=authorization_type_0)
    assert (
        f"{type(web_client_0).__module__}.{type(web_client_0).__qualname__}"
        == "pywrapid.webclient.web.WebClient"
    )
    assert web_client_0._authorization_type == authorization_type_0


def test_case_10() -> None:
    """Missing attribute for object"""
    var_0 = module_3.getlocale()
    with pytest.raises(AttributeError):
        module_0.WebClient(wrapid_config=var_0)


def test_case_11() -> None:
    """Basic auth sanity"""
    web_client_0 = module_0.WebClient()
    assert (
        f"{type(web_client_0).__module__}.{type(web_client_0).__qualname__}"
        == "pywrapid.webclient.web.WebClient"
    )
    str_0 = "p"
    str_1 = "\\A"
    basic_auth_credentials_0 = module_0.BasicAuthCredentials(str_0, str_0, str_1)
    assert (
        f"{type(basic_auth_credentials_0).__module__}.{type(basic_auth_credentials_0).__qualname__}"
        == "pywrapid.webclient.web.BasicAuthCredentials"
    )
    str_2 = "25\\jW^\x0c"
    str_3 = "\nv\x0c<`"
    module_0.BasicAuthCredentials(str_3, str_2)
    str_4 = "+)Ad"
    dict_0 = {web_client_0: str_4}
    with pytest.raises(module_1.ClientError):
        module_0.WebClient(dict_config=dict_0, wrapid_config=str_1)


def test_case_12() -> None:
    """Clean web credential"""
    web_credentials_0 = module_0.WebCredentials()
    assert (
        f"{type(web_credentials_0).__module__}.{type(web_credentials_0).__qualname__}"
        == "pywrapid.webclient.web.WebCredentials"
    )
    assert (
        f"{type(module_0.WebCredentials.options).__module__}."
        f"{type(module_0.WebCredentials.options).__qualname__}" == "builtins.property"
    )

    module_0.WebClient(credentials=web_credentials_0)


def test_case_13() -> None:
    """x509 Cert error"""
    str_0 = "\x0bs^#DH"
    with pytest.raises(module_2.ConfigurationValidationError):
        module_0.X509Credentials(str_0, str_0)


def test_case_14() -> None:
    """Cred file exception, internal properties"""
    str_0 = "p"
    file = os.path.abspath(__file__)
    basic_auth_credentials_0 = module_0.BasicAuthCredentials(str_0, str_0, str_0)
    assert (
        f"{type(basic_auth_credentials_0).__module__}.{type(basic_auth_credentials_0).__qualname__}"
        == "pywrapid.webclient.web.BasicAuthCredentials"
    )

    x509_credentials_0 = module_0.X509Credentials(file, file, str_0)
    assert (
        f"{type(x509_credentials_0).__module__}.{type(x509_credentials_0).__qualname__}"
        == "pywrapid.webclient.web.X509Credentials"
    )

    webc_0 = module_0.WebClient(credentials=basic_auth_credentials_0)
    assert webc_0._login_url == str_0
    assert webc_0._access_token == ""
    assert webc_0._config == {}
    assert webc_0._credential_options == {"auth": (str_0, str_0)}

    with pytest.raises(module_1.ClientAuthorizationError):
        module_0.WebClient(authorization_type=basic_auth_credentials_0)
    with pytest.raises(module_1.CredentialKeyFileError):
        module_0.X509Credentials(file, str_0, str_0)
    with pytest.raises(module_1.CredentialError):
        module_0.X509Credentials(str_0, file, str_0)
