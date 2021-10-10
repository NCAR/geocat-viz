# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
# sys.path.insert(0, os.path.abspath('.'))

import geocat.viz

# -- Project information -----------------------------------------------------

project = 'GeoCAT-viz'

import datetime

current_year = datetime.datetime.now().year
copyright = u'{}, University Corporation for Atmospheric Research'.format(
    current_year)
author = u'GeoCAT'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx', 
    #'sphinx.ext.mathjax'
    ]

intersphinx_mapping = {
    'python': ('http://docs.python.org/3/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
    'xarray': ('http://xarray.pydata.org/en/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
    'cartopy': ('https://scitools.org.uk/cartopy/docs/latest/', None)
    }

napoleon_use_admonition_for_examples = True
napoleon_include_special_with_doc = True

autosummary_generate = True
autoclass_content = 'both'

autodoc_default_flags = ['members', 'undoc-members', 'private-members', 'special-members', 'inherited-members', 'show-inheritance']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The version info for the project being documented
def read_version():
    for line in open('../meta.yaml').readlines():
        index = line.find('set version')
        if index > -1:
            return line[index + 15:].replace('\" %}', '').strip()

# The short X.Y version.
version = read_version()

# The full version, including alpha/beta/rc tags.
release = read_version()

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

on_rtd = os.environ.get('READTHEDOCS') == 'True'
if on_rtd:
    html_theme = 'default'
else:
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['custom']

html_logo = '_static/images/nsf.png'

# Output file base name for HTML help builder.
htmlhelp_basename = 'geocat-vizdoc'

autodoc_typehints = 'none'

# Allow for changes to be made to the css in the theme_overrides file
def setup(app):
    app.add_css_file('theme_overrides.css')
