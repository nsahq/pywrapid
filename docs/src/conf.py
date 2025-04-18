"""Configuration file for the Sphinx documentation builder.

For a full list of options see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

-- Path setup --------------------------------------------------------------

If extensions (or modules to document with autodoc) are in another directory,
add these directories to sys.path here. If the directory is relative to the
documentation root, use os.path.abspath to make it absolute, like shown here.
"""

import os
import sys
from datetime import datetime

import sphinx_rtd_theme

test_path = os.path.abspath("../")
tp = os.path.abspath(os.path.join(test_path, "../", "src"))
sys.path.insert(0, tp)
sys.path.insert(0, os.path.abspath("../../"))
sys.path.insert(0, os.path.abspath("../../src/pywrapid"))
# pylint: disable=invalid-name

# -- Project information -----------------------------------------------------

project = "pywrapid"
copyright = f"2022-{datetime.now().year}, NSAHQ"  # pylint: disable=redefined-builtin
author = "Jonas Werme"

# Use setuptools_scm to get version from git
try:
    from setuptools_scm import get_version

    version = get_version(root="../..", relative_to=__file__)
    release = version
except (ImportError, LookupError):
    # If setuptools_scm is not installed or version cannot be determined
    # (e.g., when the docs are being built on Read the Docs)
    version = "0.3.0"
    release = "0.3.0"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    # "sphinx_autodoc_typehints",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
]

autoclass_content = "both"
source_suffix = ".rst"
master_doc = "index"
add_function_parentheses = False
add_module_names = False

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "logo_only": False,
    # ToC options
    "collapse_navigation": False,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}
html_show_sourcelink = False
html_show_sphinx = True
html_show_copyright = True
html_sidebars = {
    "**": [
        "globaltoc.html",
    ]
}

htmlhelp_basename = f"{project}doc"

intersphinx_mapping = {"python": ("https://docs.python.org/3/", None)}
