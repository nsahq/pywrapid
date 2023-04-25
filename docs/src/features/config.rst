***************
Pywrapid Config
***************
Config classes that can be used through out the various pywrapid modules or as a stand alone config management util.
Currently only yaml configs is supported, with more file types in the roadmap. (Feel free to contribute with additional sypport.)

We intend to at least support the following file types:
  * YAML
  * TOML*
  * INI*
  * JSON*
  * KeyValue*

(* Not implemented yet but planned)

Two general config classes is provided: ApplicationConfig and ConfigSubSection
Both inherits the WrapidConfig class and exposes the configuration data as a dict under the "cfg" propery.


Simplicity is king and you can therefore use parts as you wish, or adopt wrapid config concept as a whole.

Configuration file discovery
----------------------------
The ApplicationConfig class can be used to explore config location for default config location and common config location for Mac, Linux and Windows.

The exploration functionality can be used standalone using ApplicationConfig.application_config_location().


Precedence of configuration files:

.. code-block:: none

    1.  Parameter passed:           config_path=<your/specified/path/to/file.cfg>
    2.  Environment variable:       APPLICATION_NAME_CONFIG_PATH
    3.  Relative path:              application_name.type
    4.  Relative path:              config.type
    3.  Configuration location:     %APPDATA%/application_name/application_name.type
    4.  Configuration location:     %APPDATA%/application_name/config.type
    5.  Configuration location:     $XDG_CONFIG_HOME/application_name/application_name.type
    6.  Configuration location:     $HOME/.application_name
    7.  Configuration location:     $HOME/.config/application_name.type
    8.  Configuration location:     /etc/application_name"
    9.  Configuration location:     /etc/application_name.type"
    10. Configuration location:     /etc/application_name/application_name.type"
    11. Configuration location:     /etc/application_name/config.type"
    12. Configuration location:     /etc/application_name/config"
    13. Configuration location:     /etc/defaults/application_name"


Configuration structure
-----------------------
A sample configuration is provided in the repo and looks as follows:

.. code-block:: yaml

    my_cool_webclient:
      url: "https://cool.server.address.nonexisting"
      password: "y0uRc00lP@55w0rd"
      key_file: "~/client.key"
      cert_file: "~/client.crt"

    some_dependency_settings:
      must_have_value: "stuff"
      search_and_destroy: True
      kill_on_sight: ["flowers", "trees", "stones"]

    logging:
      default:
        file:
          level: 40
          location: "~/my_cool_webclient-errors.log"
          format: "%(asctime)-15s (%(name)s) %(message)s"
        console:
            level: 20
      pywrapid:
        file:
          level: 10
          location: "~/pywrapid-debug.log"
      urllib3:
        console:
          level: 0

Application Configuration
-------------------------

.. autoclass:: pywrapid.config.ApplicationConfig
   :members:
   :show-inheritance:

Configuration Sub section
-------------------------
.. autoclass:: pywrapid.config.ConfigSubSection
   :members:
   :show-inheritance:

Exceptions
----------
.. autoexception:: pywrapid.config.ConfigurationException
   :show-inheritance:

.. autoexception:: pywrapid.config.ConfigurationError
   :show-inheritance:

.. autoexception:: pywrapid.config.ConfigurationValidationError
   :show-inheritance:

.. autoexception:: pywrapid.config.ConfigurationFileNotFoundError
   :show-inheritance:
