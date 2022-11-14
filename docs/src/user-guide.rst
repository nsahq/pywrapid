:orphan:

**********
User Guide
**********

pywrapid is sectioned into sublibraries with vastly different purposes and with expendability in mind.


Importing pywrapid
==================
To use a pywrpid features use explicit imports (as per best practice) like so:

.. code-block:: python

  from pywrapid.<sublibrary> import <class/function>

or

.. code-block:: python

  from pywrapid import <sublibrary>


The module structure is picked to allow for future use cases to be added with rolling updates without breaking backwards compatibillity.

Each sublibrary contains its own section in this documentation.
To have additional modules or module features added; either submit a pull request or contact NSAHQ team for help with development.


Configuration
=============
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


Config Examples
---------------
Example 1:


Logging
=======
Log settings are available through the application configuration file.

The logging framework allows you to control log levels for separate loggers, including
other packages being used as part of the application.

For normal usage it will probably be enough to configure default logging to info level (see configuration section for reference).
The following log possibillities exist:

  * Console   - logs to standard out and standard err
  * File      - log to a file location, for syslog logging in linux set this to /dev/syslog (journal can be configured to capture standard out as well)

To do more advaced logging on a per module level, please see the `advanced logging<features/log#Advanced Logging>` section under developer-guide.

.. list-table:: Log levels
   :widths: 50 50 50
   :header-rows: 1

   * - Log level
     - Config value
     - Logging enum
   * - Disabled
     - 0
     - -
   * - DEBUG
     - 10
     - logging.DEBUG
   * - INFO
     - 20
     - logging.INFO
   * - WARNING
     - 30
     - logging.WARNING
   * - ERROR
     - 40
     - logging.ERROR
   * - CRITICAL
     - 50
     - logging.CRITICAL

If you have the logging section in your config file and decide not to override defaults you will have the following defaults applied settings:

.. code-block:: yaml

    console:
        format: "[%(levelname)s] (%(name)s) %(message)s"
        level: logging.INFO
    file:
        format: "%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s"
        level: logging.INFO
        location: ""

If file logging is used and a location is not set either in default or as a module specific setting, the file handler will not be set up.


Log format
----------
Format of the produced logs can be set for each output stream you configure.
The default section sets the default format for all subsequent modules, but can be overridden on a per module basis if so desired.

If left unset the following will be the default format:

Console:
[%(levelname)s] (%(name)s) %(message)s

File:
%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s

The name showing in the logfiles within () (parentheses) is the . (dot) notation you can use in the configuration file to target a specific modules logger.


Exit codes
==========
The scripts have custom exit codes to indicate specific errors.

.. code-block:: none

    Exit codes:
    0 - Success
    1 - Run time error
    2 - Initialization error of config and logging
    3 - Authentication error
    4 - API action error
    5 - Termination signal recieved but cleanup failed
    6 - Script execution aborted with cleanup successful
    7 - Data state does not allow continuation



Folder structure
================
pywrapid and its sub libraries use the following folder structure:


.. code-block:: none

    pywrapid
    ├───src
    │   ├───pywrapid
    │   │   ├───sublibrary1
    │   │   │   ├───exceptions.py
    │   │   │   ├───library_code_1.py
    │   │   │   ├───library_code_n.py
    │   │   │   └───requirements.txt
    │   │   ├───sublibrary2
    │   │   │   ├───exceptions.py
    │   │   │   ├───library_code_1.py
    │   │   │   ├───library_code_n.py
    │   │   │   └───requirements.txt
    │   │   ├───sublibraryN
    │   │   │   ├───exceptions.py
    │   │   │   ├───library_code_1.py
    │   │   │   ├───library_code_n.py
    │   │   │   └───requirements.txt
    ├───docs
    │   ├───src
    │   │   ├───documentation-file1.rst
    │   │   ├───documentation-fileN.rst
    │   │   ├───conf.py
    ├───tests
    │   ├───test_pywrapid_modulename_filename1.py
    │   ├───test_pywrapid_modulename_filenameN.py
    │   ├───test_integration_testgroup1.py
    │   ├───test_integration_testgroupN.py
    │   ├───test_user_testgroup1.py
    │   ├───test_user_testgroupN.py
    ├───tox.ini
    ├───requirements
    ├───pyproject.toml
