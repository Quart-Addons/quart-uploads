# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys, os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.append(os.path.join(os.path.dirname(__file__), '_themes'))
sys.path.insert(0, os.path.abspath('../..'))
sys.path.append(os.path.abspath('..'))
module_path = os.path.join(os.path.dirname(__file__), '../quart_bcrypt.py')
with open(module_path) as module:
    for line in module:
        if line.startswith('__version_info__'):
            package_version = '.'.join(eval(line.split('__version_info__ = ')[-1]))
            break

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Quart-Uploads'
copyright = '2022, Chris Rood'
author = 'Chris Rood'
version = package_version
release = package_version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.napoleon','sphinx.ext.autodoc']

autodoc_default_options = {
    'member-order': 'bysource',
}

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
