import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.abspath(".."))

from restfly import __version__ as version

project = "RESTfly"
copyright = f"{datetime.now().year}, Steve McGrath"
author = "Steve McGrath"
release = version
html_theme = "furo"
html_static_path = ["_static"]
html_theme_options = {
    "light_logo": "logo-light-mode.svg",
    "dark_logo": "logo-dark-mode.svg",
}

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",
    "sphinx.ext.extlinks",
    "sphinxcontrib.mermaid",
]

autodoc_default_options = {
    "inherited-members": True,
    "members": True,
    "private-members": True,
    #    "member-order": "groupwise",
}

autodoc_typehints = "description"


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
