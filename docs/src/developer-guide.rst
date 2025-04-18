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


CI/CD Pipeline
==============

The project uses a streamlined CI/CD pipeline based on GitHub Actions to ensure code quality
and simplify the release process.

Validation Workflow
-------------------

We use a centralized validation workflow that intelligently orchestrates various checks:

- **Linting**: Code style and quality checks
- **Testing**: Unit and integration tests
- **Documentation**: Validates documentation builds correctly
- **Security**: Vulnerability scanning

The key workflow files are:

- ``validate-changes.yml``: Orchestrates which checks to run based on changed files
- ``test.yml``, ``lint.yml``, ``docs.yml``, ``security.yml``: Specialized workflows

The validation workflow runs automatically on:

- Pull requests
- Direct pushes to main branches

You can also manually trigger validation checks through GitHub Actions.

Release and Publishing Process
==============================

Pywrapid uses GitHub-integrated release process that leverages GitHub Actions along with
automatic release notes generation.

Version Management
------------------

The project uses ``setuptools_scm`` for version management, which means:

1. Version numbers are automatically derived from Git tags
2. No manual version number updates needed in code
3. Git tags determine the package version

Creating a New Release
----------------------

To create a new release:

1. Go to the GitHub repository page
2. Click on "Releases" in the right sidebar
3. Click "Draft a new release"
4. Create a new tag following semantic versioning (e.g., ``v1.2.3``)
5. Add a release title (optional)
6. GitHub will auto-generate release notes based on merged PRs
7. Click "Publish release"

The publish workflow will automatically:

- Run all validation checks
- Build the package
- Publish the package to PyPI
- Attach build artifacts to the GitHub release

Automatic Release Notes
-----------------------

Release notes are automatically generated based on merged pull requests since the last release.
To ensure your changes are properly categorized:

1. **Add labels to your PRs**:

   - ``feature`` or ``enhancement``: For new features
   - ``bug`` or ``fix``: For bug fixes
   - ``docs``: For documentation changes
   - ``maintenance`` or ``refactor``: For code maintenance
   - ``dependencies`` or ``deps``: For dependency updates

2. **Use descriptive PR titles**: These become part of the release notes

Testing the Release Process
---------------------------

You can test different parts of the release process without actually publishing:

1. Go to the GitHub Actions tab
2. Select the "Publish" workflow
3. Click "Run workflow"
4. Select one of the following options:

   - ``validate-only``: Just runs the validation checks
   - ``build-only``: Builds the package without publishing
   - ``draft-release-notes``: Generates a draft release with notes


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
