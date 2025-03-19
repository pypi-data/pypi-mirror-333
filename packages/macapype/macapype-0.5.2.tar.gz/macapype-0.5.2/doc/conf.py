# -*- coding: utf-8 -*-
#
# macapype documentation build configuration file, created by
# sphinx-quickstart on Tue Nov 27 18:47:41 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from datetime import date
import sphinx_gallery  # noqa
from sphinx_gallery.sorting import FileNameSortKey
import sphinx_bootstrap_theme

# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'numpydoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx_gallery.gen_gallery',
    'sphinxcontrib.fulltoc'
]

# generate autosummary even if no references
autosummary_generate = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'macapype'
td = date.today()
copyright = u'%s, Macapype Developers (macatools). Last updated on %s' % (td.year,
                                                                td.isoformat())

author = 'Macapype Developers (macatools)'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

import macapype
# The short X.Y version.
version = macapype.__version__

# The full version, including alpha/beta/rc tags.
release = macapype.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_logo = "img/logo/logo_macapype_0.3.jpg"

html_sidebars = {'**': ['localtoc.html'],
   'using/windows': ['windowssidebar.html']}

html_theme_options = {
    'navbar_title': 'Macapype',
    'bootswatch_theme': "flatly",
    'navbar_sidebarrel': False,
    'bootstrap_version': "3",
    'navbar_links': [
        ("Gallery", "auto_examples/index"),
        ("API", "api"),
        ("Tutorial", "tutorial"),
        ("Installation", "install"),
        ("Github", "https://github.com/macatools/macapype", True),
    ]
    }

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'macapypedoc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_elements = {
    #'papersize': 'a4paper',
    'papersize': 'letterpaper',
    'pointsize': '12pt',
    'preamble': r'''
    \usepackage[none]{hyphenat}
    \usepackage[document]{ragged2e}
    '''
}


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'macapype.tex', 'macapype Documentation',
     'David Meunier', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'macapype', 'macapype Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'macapype', 'macapype Documentation',
     author, 'macapype', 'One line description of project.',
     'Miscellaneous'),
]

intersphinx_mapping = {'python': ('https://docs.python.org/', None)}

sphinx_gallery_conf = {
    'examples_dirs': '../examples',
    'gallery_dirs': 'auto_examples',
    'filename_pattern': '^((?!sgskip).)*$',
    'backreferences_dir': 'generated',
    'within_subsection_order': FileNameSortKey,
    'reference_url': {
        'numpy': 'http://docs.scipy.org/doc/numpy-1.9.1',
        'scipy': 'http://docs.scipy.org/doc/scipy-0.17.0/reference',
        'nipype': 'https://nipype.readthedocs.io/en/latest',
        'macapype': 'http://macatools.github.io/macapype/'
    }
}

import sys
import os.path as op

path = op.join(op.dirname(__file__), '../examples/')
sys.path.insert(0, path)

#from visbrain.config import CONFIG
#CONFIG['MPL_RENDER'] = True
