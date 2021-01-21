# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# --- Autodoc ----------------------------------------------------------------
import sys
autodoc_mock_imports = ['td', 'td.op']

project = 'RTFM2'
copyright = '2020, Akeem The Dream'
author = 'Akeem The Dream'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc','sphinx.ext.napoleon','sphinx.ext.autodoc.typehints']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []



autodoc_default_options = {
    'members': True,
    'member-order': 'groupwise', # bysource groupwise alphabetical
    #'special-members': '__init__',
    #'undoc-members': True,
    'inherited-members': False,
    'show-inheritance':False,
    'exclude-members': '__weakref__'
}

autodoc_typehints = 'description'


# -- Options for HTML output -------------------------------------------------

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_theme_options_rtd = {
    'canonical_url': '',
    'analytics_id': '',  #  Provided by Google in your dashboard
    'logo_only': True,
    'display_version': False,
    'prev_next_buttons_location': 'top',
    'style_external_links': False,
    'style_nav_header_background': 'black',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': True
}

# The theme to use for HTML and HTML Help pages.  See the documentation for
html_theme = 'sphinx_rtd_theme' 
html_theme_options = html_theme_options_rtd 