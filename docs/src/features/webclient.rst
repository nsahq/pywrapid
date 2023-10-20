******************
Pywrapid Webclient
******************
Documentation coming soon

Configuration
-------------

Client settings:
client_options: request options such as ssl settings, timeout etc.

Token settings:
refresh_token_timeout: Time the auth provider specifies for refresh token expiry in seconds <default: 86400>
access_token_timeout: The time for access token expiry in seconds, omit or set to 0 to use response body values from auth provider <default: 0>
token_expiry_offset: Seconds before expiration time we will treat tokens as already expired to trigger early renewal <default: 10>
access_token_header: Custom response header name to look for access token after authentication <default: ''>

Any additional configuration parameter passed in will be included in the credential objects config.
Same goes for any extra key value pair passed as parameter at instantiation.


Webclient
---------

.. autoclass:: pywrapid.webclient.WebClient
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__
   :private-members: _unpack_jwt

Credentials
-----------
.. autoclass:: pywrapid.webclient.WebCredentials
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywrapid.webclient.BasicAuthCredentials
   :members:
   :undoc-members:
   :show-inheritance:

.. autoclass:: pywrapid.webclient.X509Credentials
   :members:
   :undoc-members:
   :show-inheritance:

Client Exceptions
-----------------
.. autoexception:: pywrapid.webclient.ClientException
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientAuthorizationError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientAuthenticationError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientTokenRefreshError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientTimeout
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientConnectionError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientHTTPError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.ClientURLError
   :show-inheritance:
   :members:

Credential Exceptions
---------------------

.. autoexception:: pywrapid.webclient.CredentialException
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.CredentialError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.CredentialCertificateFileError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.CredentialKeyFileError
   :show-inheritance:
   :members:

.. autoexception:: pywrapid.webclient.CredentialURLError
   :show-inheritance:
   :members: