********
pywrapid
********

.. image:: https://readthedocs.org/projects/pywrapid/badge/?version=latest
    :target: https://pywrapid.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status


This library is created to wrap other popular libraries and extend their functionalities
for rapid development of python applications.
Includes configuration management compatible with all other modules provided in pywrapid.

Extend functionality as you wish by wrapping the modules and/or inheriting the classes.

Features
========

pywrapid.config
---------------

Config classes that can be used through out the various pywrapid modules or as a stand alone config management util.
Currently only yaml configs is supported, with more file types in the roadmap. (Feel free to contribute with additional sypport.)

We intend to at least support the following file types:
    - YAML
    - TOML*
    - INI*
    - JSON*
    - KeyValue*

(* Not implemented yet but planned)

Two general config classes is provided: ApplicationConfig and ConfigSubSection
Both inherits the WrapidConfig class and exposes the configuration data as a dict under the "cfg" propery.

The ApplicationConfig class can be used to explore config location for default config location and common config location for Mac, Linux and Windows.

The exploration functionality can be used standalone using ApplicationConfig.application_config_location().

Simplicity is king and you can therefore use parts as you wish, or adopt wrapid config concept as a whole.

Dependencies
------------

    - PyYAML

### pywrapid.webclient
Extends the well known requests library.
Principle behind the web client is to give you one base that can be used in the same manner regardless of the mix and match between Authorization and Authentication methods used by the API/website.
If a new version of the API your client consumes comes out with a different authentication method, you should only have to instanciate a different class to match the API and have it work again.

Gives you a generic web client class you can use as a base for your client creations.

Credential types:

    - No authentication
    - Basic Auth
    - x509

Authorization types:

    - NONE
    - BASIC
    - BEARER
    - JWT
    - OAUTH2

pywrapid.log
============

Helper functions for setting up and controlling the defacto standard logging framework "logging".

Allows you to easily configure logging handlers (currently only console and file) on a per module basis.

Gives your application a similar configuration principle to djangos log management, where you can control logging for each import or derived modules.
You can specify different log level or formats per module and per handler.
Propagation to parent will not take place for modules you specify, giving you the control, while also being able to capture undefined child loggers.


See documentation for more information.

Dependencies
------------

    - pyjwt

Exceptions
----------

Each sub library comes with pywrapid exceptions.
The exceptions will normalize multiple wrapped libraries/tools and extend with additional generic exceptions.


Dependencies
============

    - pyyaml
    - requests
    - pyjwt

Needed softwares
================

    - python3.x