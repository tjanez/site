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

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Theme
THEME = 'Flex'
SITETITLE = SITENAME
SITESUBTITLE = 'Systems Engineer, DevOps'
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
