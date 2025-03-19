# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.insert(0, str(Path("../../src").resolve()))

from packaging.version import Version

import ppftpy

full_version = ppftpy.__version__
version_obj = Version(full_version)

project = "ppft-py"
author = "Jannik Schäfer"
copyright = "2025, Jannik Schäfer"  # noqa: A001
release = full_version
version = f"{version_obj.major}.{version_obj.minor}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.doctest",
    "numpydoc",
    "sphinx_design",
    "sphinx_copybutton",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/jnk22/ppft-py",
            "icon": "fab fa-github-square",
        }
    ]
}
html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

napoleon_numpy_docstring = True
