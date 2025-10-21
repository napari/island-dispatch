# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'napari blog'
copyright = '2024, The napari community'
author = 'The napari community'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "ablog",
    "sphinx.ext.intersphinx",
]

templates_path = ['_templates']
exclude_patterns = [
    "README.md",
]

# ABlog configuration
blog_baseurl = "https://napari.org"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'napari_sphinx_theme'
html_static_path = ['_static']
html_logo = "_static/logo.png"
html_favicon = "_static/logo.png"

html_theme_options = {
    #"external_links": [{"name": "napari hub", "url": "https://napari-hub.org"}],
    "github_url": "https://github.com/napari/napari",
    "navbar_start": ["navbar-logo", "navbar-project"],
    "navbar_end": ["navbar-icon-links", "theme-switcher"],
    "navbar_persistent": [],
    "header_links_before_dropdown": 6,
    # "secondary_sidebar_items": ["page-toc"],
    "pygment_light_style": "napari",
    "pygment_dark_style": "dracula",
    # "announcement": "https://napari.org/dev/_static/announcement.html",
    "analytics": {
        # The domain you'd like to use for this analytics instance
        "plausible_analytics_domain": "napari.org",
        # The analytics script that is served by Plausible
        "plausible_analytics_url": "https://plausible.io/js/plausible.js",
    },
}
