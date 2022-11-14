************
Pywrapid Log
************
Log settings are available through the application configuration file.

The logging framework allows you to control log levels for separate loggers, including
other packages being used as part of the application.

For normal usage it will probably be enough to configure default logging to info level (see user-guide configuration section for reference).
The following log possibillities exist:
* Console   - logs to standard out and standard err
* File      - log to a file location, for syslog logging in linux set this to /dev/syslog (journal can be configured to capture standard out as well)

To do more advaced logging on a per module level you can configure debug logging for individual modules/packages used.

Usage example
-------------

Example 1 - passing dict:

.. code-block:: python

    from pywrapid.log import application_logging
    application_logging(
        {
            "default": {
                "console": {
                    "level": 10
                }
            }
        }
    )
    log.debug("logging initalized with debug level set as default")


Example 1 - using "logging" as a pywrapid config sub section in yaml file:

.. code-block:: python

    from pywrapid.config import ApplicationConfig, ConfigSubSection
    from pywrapid.log import application_logging

    app_conf = ApplicationConfig(
            application_name=__name__,
            file_type="yml",
            allow_config_discovery=True,
        )

    if "logging" in app_conf.cfg:
        log_config = ConfigSubSection(app_conf, "logging")
        application_logging(
            log_config,
        )

For config file example, please see :ref: `logging section of user guide <Logging>` and/or :ref: `configuration section <Configuration structure>`.

General
-------
By specifiying a module in the configuration, you will get a logger created with:
* Propagation to parent turned off
* Log level you specify (if left out the default log level value will be set instead)

The defined loggers will automatically be adjusted to the lowest logging level you set for handlers.
Log propagation has been turned off for all activated loggers.

When you turn debugging on for a module, it will activate logging for all derived loggers (all imported/called python modules)
However, you still have the control of the derived loggers by specifying them in their own section.

This is usefull if you import a library that is very verbose when it comes to debug logging.
You can control that library by simply adding the name to the logging section and setting the log level 0 or the level of your choice.

Controlling a specific submodule of a package is also possible by using the . (dot) notation of the names.
E.g. if we import package X and it has sub modules (or imports other packages) that produce logs, lets call them subY and impZ, we can change the log level for the specific module
by adding "x.subY:" or "impZ" in the logging section respectively. This will give us a logger for that module that we can set our desired behaviour for.

To mute logging of "subY" and allow debug in console from "impZ" and the main "x" module, we can specify:

.. code-block:: yaml

    logging:
        default:
            console:
                level: 20
        x:
            console:
                level: 10
        x.subY:
            console:
                level: 0
        impZ:
            console:
                level: 10



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


File logging
------------
Each logger created can also have a file output, with level independently controlled from the console logging.
This means you can turn debug logging on for any module and only have that output turn up in a file of your choice.

File logging can be used to write messages to syslog in linux systems by targetting /dev/syslog as the file location.
Do not that this would bypass journal if your system is using systemd with journal as the logging system.

More advanced file output use cases could be that you specifiy a set up modules you want debug logging for and set them to output to the same file for the troubleshooting session at hand.

If a location is not set either in default or as a module specific setting, the file handler will not be set up.

Console logging
---------------
Console logging section of each module allows you to set the messages for logg level that should be written to standard out/standard err.

Journal (systemd) can usually capture this type of output when the application is run as a service.
Journal can also be configured to print captured output to syslog.


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



Technical Log Documentation
---------------------------

.. automodule:: pywrapid.log.application_log
   :members:
   :undoc-members:
   :show-inheritance: