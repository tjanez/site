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
    # custom CSS
    'extra/custom.css',
    # GitHub Pages custom domain
    'extra/CNAME',
]
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'},
    'extra/CNAME': {'path': 'CNAME'},
}

# Enable Admonition Markdown extension
default_md_extensions = ['codehilite(css_class=highlight)', 'extra']
MD_EXTENSIONS = default_md_extensions + ['admonition']

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
