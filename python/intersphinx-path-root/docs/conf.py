"""Configuration file for Sphinx.

See: https://www.sphinx-doc.org/en/master/usage/configuration.html
"""
# pylint:disable=invalid-name
# Sphinx expects names like this.
author = "Jeremy Audet"
copyright = "2020, Jeremy Audet"  # pylint:disable=redefined-builtin
exclude_patterns = ["_build"]
extensions = ["sphinx.ext.intersphinx"]
nitpicky = True
project = "intersphinx-path-root"

intersphinx_mapping = {
    "intersphinx-path-1": (
        "/plugins/intersphinx-path-1",
        "../plugins/intersphinx-path-1/docs/_build/html/objects.inv",
    ),
    "intersphinx-path-2": (
        "/plugins/intersphinx-path-2",
        "../plugins/intersphinx-path-2/docs/_build/html/objects.inv",
    ),
}
