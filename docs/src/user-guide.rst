:orphan:

**********
User Guide
**********

pywrapid is sectioned into sublibraries with vastly different purposes and with expendability in mind.


Getting started
===============

Install pywrapid from pypi

.. code-block:: bash

    pip install pywrapid


or from git

.. code-block:: bash

    pip install git+https://github.com/nsahq/pywrapid.git


or build from source

.. code-block:: bash

    git clone https://github.com/nsahq/pywrapid.git
    cd pywrapid
    pip install build
    python -m build
    pip install dist/pywrapid*.whl


Importing pywrapid
------------------
To use a pywrpid features use explicit imports (as per best practice) like so:

.. code-block:: python

  from pywrapid.<sublibrary> import <class/function>

or

.. code-block:: python

  from pywrapid import <sublibrary>


The module structure is picked to allow for future use cases to be added with rolling updates without breaking backwards compatibillity.

Each sublibrary contains its own section in this documentation.
To have additional modules or module features added; either submit a pull request or contact NSAHQ team for help with development.
