# NOTE: The content of this file is over-ridden by publishconf.py when
# publishing, so ensure you also check that file.

import datetime
import hashlib

import pymdownx.emoji

AUTHOR = 'Tadej Janež'
SITEURL = 'http://localhost:8000' # NOTE: This is set to the actual site URL in publishconf.py.
SITENAME = 'Tadej Janež'
SITETITLE = SITENAME
SITESUBTITLE = 'Passionate about DevOps, Python and OSS'

SITELOGO = '/images/profile.png'
COPYRIGHT_NAME = AUTHOR
copyright_year_start = 2016
copyright_year_end = datetime.date.today().year
if copyright_year_end == copyright_year_start:
    COPYRIGHT_YEAR = copyright_year_start
else:
    COPYRIGHT_YEAR = '{}-{}'.format(copyright_year_start, copyright_year_end)

PATH = 'content'

TIMEZONE = 'Europe/Ljubljana'

DEFAULT_LANG = 'en'

# Atom feeds
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/category-{slug}.atom.xml'
TAG_FEED_ATOM = 'feeds/tag-{slug}.atom.xml'

# Social links
SOCIAL = (
    ('github', 'https://github.com/tjanez'),
    ('linkedin', 'https://www.linkedin.com/in/tadej-janez/'),
    ('x-twitter', 'https://x.com/TadejJanez'),
    ('rss', '/feeds/all.atom.xml')
)

# Main menu
MAIN_MENU = True
MENUITEMS = (
    ("Archives", "/archives.html"),
    ("Categories", "/categories.html"),
    ("Tags", "/tags.html"),
)

DEFAULT_PAGINATION = 10

STATIC_PATHS = [
    'images',
    'scripts',
    # custom CSS
    'extra/custom.css',
    # GitHub Pages custom domain
    'extra/CNAME',
]
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/CNAME': {'path': 'CNAME'},
}

# Markdown
MARKDOWN = {
    # Markdown Extensions configuration
    'extension_configs': {
        # Pelican defaults — must be kept since defining MARKDOWN replaces them.
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
        # Enable Admonition Markdown extension to enable adding rST-style
        # admonitions to Markdown documents.
        'markdown.extensions.admonition': {},
        # Enable Table of Contents Markdown extension to create a unique link
        # anchor for each heading.
        'markdown.extensions.toc': {'permalink': True},
        # Enable PyMdown Emoji, a 3rd party Python Markdown extension, to be able
        # to use emojis.
        'pymdownx.emoji': {
            'emoji_generator': pymdownx.emoji.to_svg,
            'options': {
                'attributes': {
                    'align': 'absmiddle',
                    'height': '20px',
                    'width': '20px',
                },
            },
        },
    },
    # Also Pelican default that needs to be manually carried over.
    'output_format': 'html5',
}

# Theme
from pelican.themes import reflex
THEME = reflex.path()
THEME_COLOR = 'dark'
THEME_COLOR_AUTO_DETECT_BROWSER_PREFERENCE = True
# Add ability to toggle light/dark manually for the site (and override browser
# preference).
THEME_COLOR_ENABLE_USER_OVERRIDE = True

# CSS customizations
CUSTOM_CSS = 'static/custom.css'

# Code highlighting
PYGMENTS_STYLE = 'tango'
PYGMENTS_STYLE_DARK = 'stata-dark'


# License
CC_LICENSE = {
    "name": "Creative Commons Attribution-ShareAlike",
    "version": "4.0",
    "slug": "by-sa"
}

# Plugins
PLUGINS = [
    # Unofficial community repackaging of the Summary plugin.
    # NOTE: The official Summary plugin at
    # https://github.com/getpelican/pelican-plugins/tree/master/summary has not
    # been migrated to the new https://github.com/pelican-plugins GitHub
    # organization yet.
    'minchin.pelican.plugins.summary'
]

# External integrations
GOOGLE_ANALYTICS = 'UA-85987058-1'
DISQUS_SITENAME = 'tadejjanez'
