import datetime
import hashlib

AUTHOR = 'Tadej Janež'
SITENAME = 'Tadej Janež'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Ljubljana'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

SOCIAL = (
    ('github', 'https://github.com/tjanez'),
    ('twitter', 'https://twitter.com/TadejJanez'),
    ('rss', '//tadej.ja.nez.si/feeds/all.atom.xml')
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

# Default MARKDOWN setting
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}

# Enable Admonition Markdown extension to enable adding rST-style
# admonitions to Markdown documents.
MARKDOWN['extension_configs']['markdown.extensions.admonition'] = {}
# Enable Table of Contents Markdown extension to create a unique link
# anchor for each heading
MARKDOWN['extension_configs']['markdown.extensions.toc'] = {}

# Theme
THEME = 'Flex'
SITETITLE = SITENAME
SITESUBTITLE = 'DevOps Engineer'
email = 'tadej.j@nez.si'.encode('utf-8')
SITELOGO = 'https://seccdn.libravatar.org/avatar/{}?s=256'.format(
    hashlib.md5(email.strip().lower()).hexdigest())
copyright_year_start = 2016
copyright_year_end = datetime.date.today().year
if copyright_year_end == copyright_year_start:
    COPYRIGHT_YEAR = copyright_year_start
else:
    COPYRIGHT_YEAR = '{}-{}'.format(copyright_year_start, copyright_year_end)
PYGMENTS_STYLE = 'native'
CUSTOM_CSS = 'static/custom.css'

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['summary']

# External integrations
GOOGLE_ANALYTICS = 'UA-85987058-1'
