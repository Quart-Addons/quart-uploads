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
html_logo = "_static/logo_short.png"
html_theme_path = ['_themes']
html_static_path = ['_static']
htmlhelp_basename = 'QuartUploadsdoc'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "external_links": [
        {"name": "Source code", "url": "https://github.com/Quart-Addons/quart-uploads"},
        {"name": "Issues", "url": "https://github.com/Quart-Addons/quart-uploads/issues"},
    ],
    "icon_links": [
        {
            "name": "Quart Add-Ons",
            "url": "https://github.com/Quart-Addons",
            "icon": "fab fa-github",
        },
        {
            "name": "Quart",
            "url": "https://quart.palletsprojects.com/",
            "icon": "_static/quart.png",
            "type": "local",
        },
    ],
}

html_sidebars = {
    "index": [],
}
latex_documents = [
  ('index', 'Quart-Uploads.tex', 'Quart-Uploads Documentation',
   'Chris Rood', 'manual'),
]

latex_documents = [
  ('index', 'Quart-Uploads.tex', 'Quart-Uploads Documentation',
   'Chris Rood', 'manual'),
]
