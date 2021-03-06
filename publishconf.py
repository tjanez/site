# This file is only used if you use `fab preview` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://tadej.ja.nez.si'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/category-%s.atom.xml'
TAG_FEED_ATOM = 'feeds/tag-%s.atom.xml'
