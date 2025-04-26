# Configuration file for the Sphinx documentation builder.

import os
import sys

# Add the project source directory to the Python path
sys.path.insert(0, os.path.abspath('../src'))

# Project information
project = 'StatefulPy'
copyright = '2023, StatefulPy Team'
author = 'StatefulPy Team'
version = '0.1.0'
release = '0.1.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# HTML output configuration
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Intersphinx configuration
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# autodoc configuration
autodoc_member_order = 'bysource'
autoclass_content = 'both'
