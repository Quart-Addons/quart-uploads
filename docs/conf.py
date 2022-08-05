# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os 
import sys 

sys.path.insert(0, os.path.abspath("../"))

project = 'Quart-Uploads'
copyright = '2022, Chris Rood'
author = 'Chris Rood'
version = '0.0.1'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.napoleon','sphinx.ext.autodoc']

autodoc_default_options = {
    'member-order': 'bysource',
}

autodoc_mock_imports = [""]
templates_path = ['_templates']
exclude_patterns = ['_build']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_theme_path = ['_themes']
html_static_path = ['_static']
htmlhelp_basename = 'Quart-Uploadsdoc'

latex_documents = [
  ('index', 'Quart-Uploads.tex', 'Quart-Uploads Documentation',
   'Chris Rood', 'manual'),
]

latex_documents = [
  ('index', 'Quart-Uploads.tex', 'Quart-Uploads Documentation',
   'Chris Rood', 'manual'),
]
