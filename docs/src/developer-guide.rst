***************
Developer Guide
***************


Each library is built as a standalone library, allowing you use them individually.
The sub libraries must use pywrapid libraries where wrappers already exist and should be compatible with pywrapid config.

Functions deemed useful for other users of pywrapid should go to utils.

Keep in mind:
- Do not mix other fixes or features into your feature branch, keep it canonical
- Rebase if you fall behind
- Make sure you tests cover your changes and tox reports all green before you send a pull request
- Force push is not allowed, by anyone


To build a wheel:

.. code-block:: bash

    pip install tox
    tox

or

.. code-block:: bash

    pip install build
    python -m build


Linting and tests
=================

  - Tests should be created for all new functionality
  - Feature branch must pass linting and tests before pull request is made
  - Builds will run tox, and so should you

Linters used:

  - pylint
  - flake8
  - mypy
  - black
  - isort
  - bandit

Test suite:

  - pytest


Project structure
=================
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
    │   │   └───conf.py
    ├───tests
    │   ├───test_pywrapid_modulename_filename1.py
    │   ├───test_pywrapid_modulename_filenameN.py
    │   ├───test_integration_testgroup1.py
    │   ├───test_integration_testgroupN.py
    │   ├───test_user_testgroup1.py
    │   └───test_user_testgroupN.py
    ├───tox.ini
    ├───requirements.txt
    └───pyproject.toml
