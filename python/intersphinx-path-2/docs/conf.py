"""Configuration file for Sphinx.

See: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# pylint:disable=invalid-name
# Sphinx expects names like this.
author = "Jeremy Audet"
copyright = "2020, Jeremy Audet"  # pylint:disable=redefined-builtin
exclude_patterns = ["_build"]
extensions = ["sphinx.ext.autodoc", "sphinx.ext.intersphinx"]
nitpicky = True
project = "intersphinx-path-2"

intersphinx_mapping = {
    "intersphinx-path-1": (
        "/plugins/intersphinx-path-1",
        "../../intersphinx-path-1/docs/_build/html/objects.inv",
    ),
}
