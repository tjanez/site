Title: Setting up a Pelican site with Python 3 and Fabric on Fedora 24
Date: 2016-10-08 10:16
Category: Site
Tags: pelican, fedora, python, fabric, site
Slug: setting-up-pelican-site

According to [StaticGen](https://www.staticgen.com/), [Pelican](
http://getpelican.com/) is the most popular static site generator written in
[Python](https://www.python.org/). As of Oct 10, 2016 it has
[6168 stars on GitHub](https://github.com/getpelican/pelican).

In this blog post, I'll show you how to create your own Pelican site, track
it in a [git](https://git-scm.com/) repository, use [Fabric](
http://www.fabfile.org/) to administer it, change site's default theme and
finally, create a Hello World blog post.

## Installing prerequisites

!!! note

    This example uses a vanilla [Fedora 24 Cloud](
    https://getfedora.org/en/cloud/) system.

Install Pelican (Python 3 version), git and Fabric (unfortunately,
[only Python 2 version is currently available](
http://fedora.portingdb.xyz/pkg/fabric/)):
```
sudo dnf -y install python3-pelican git fabric
```

## Creating a git repository for the site

Create a directory for the site:
```
mkdir my-site
cd my-site
```

To setup a Pelican skeleton for the site, run `py3-pelican-quickstart` and
answer the questions. If you are unsure, you can safely accept the default
answer.

Before initializing the git repository, clean up the generated skeleton.
Remove the `Makefile` and edit `fabfile.py` to remove the unnecessary
functionality and make it work with Python 3 version of Pelican.

All `pelican` commands need to be replaced with `py3-pelican`. In addition,
the `serve()` function needs to be rewritten since it tries to directly import
the Python 2 version of `pelican.server` which is not available. You can also
safely remove the parts connected with Rackspace Cloud Files, rsync publishing
and [GitHub Pages](https://pages.github.com/) (I'll describe how to add support
for it in a follow-up blog post).

The cleaned-up version of `fabfile.py` should look something like:
```python
from fabric.api import *
import fabric.contrib.project as project
import os
import shutil

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'

# Port for `serve`
PORT = 8000

def clean():
    """Remove generated files"""
    if os.path.isdir(env.deploy_path):
        shutil.rmtree(env.deploy_path)
        os.makedirs(env.deploy_path)

def build():
    """Build local version of site"""
    local('py3-pelican -s pelicanconf.py')

def rebuild():
    """`clean`, then `build`"""
    clean()
    build()

def regenerate():
    """Automatically regenerate site upon file modification"""
    local('py3-pelican -r -s pelicanconf.py')

def serve():
    """Serve site at http://localhost:PORT/"""
    with lcd(env.deploy_path):
        local('python3 -m pelican.server {}'.format(PORT))

def reserve():
    """`build`, then `serve`"""
    build()
    serve()

def preview():
    """Build production version of site"""
    local('py3-pelican -s publishconf.py')
```

Since we are using the Python 3 version of Pelican, we can remove the Python 2
compatibility headers from `pelicanconf.py` and `publishconf.py`:
```python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
```
In addition, remove the shebang from `publishconf.py`.

Initialize the git repository and create the initial commit:
```
git init
git add *.py
git commit -m "Initial site created with pelican-quickstart"
```

!!! note

    If you use git for the first time, you must configure your git email and
    user name with:

        ::bash
        git config --global user.email "<your-email-address>"
        git config --global user.name "<your-name>"

To instruct git to ignore the generated Python byte-code and the generated
site, create `.gitignore` file with the following contents:

```
# ignore Python byte-code
*.pyc

# ignore generated site
/output/
```

and commit it with:

```
git add .gitignore
git commit -m "Add .gitignore"
```

## Administering the site with Fabric

Fabric is a Python library and a command-line tool for automating deployment
and system administration tasks. By default, it looks for a `fabfile.py` file
where one can define Fabric's tasks. See the `fabfile.py` code listing above
to get a glimpse of how Fabric tasks look like.

To run Fabric tasks, just execute `fab` followed by the task's name, e.g.
`serve`. Here are a couple of tasks that you will typically use when
administering a site.

To generate the site, use:
```
fab build
```

To serve the site locally on port 8080, use:
```
fab serve
```

To regenerate the site and serve it locally, use:
```
fab reserve
```

To automatically regenerate the site upon file modification and serve it
locally, run the following commands in two separate terminals:
```
fab regenerate
fab serve
```

## Changing site's default theme

Frankly speaking, the default Pelican theme looks dated nowadays, so you'll
want to change it sooner rather than later.
Take a look at the [Pelican Themes site](http://www.pelicanthemes.com/) and
find a theme you like.

After you decide which theme you'll use (in the example I'll use [Alexandre
Vicenzi's Flex theme](https://github.com/alexandrevicenzi/Flex/), which I use
for my Pelican site), add it to your git repo as a submodule:
```
git submodule add https://github.com/alexandrevicenzi/Flex.git Flex
```

Then configure it in `pelicanconf.py`.

!!! note

    Each theme has its own configuration. Consult the chosen theme's
    documentation on what you can configure.

Here is an example configuration for the Flex theme:
```python
import datetime
import hashlib

... other configuration ...

# Theme
THEME = 'Flex'
SITETITLE = SITENAME
SITESUBTITLE = 'My cool descrition'
email = 'my.email@somedomain.com'.encode('utf-8')
SITELOGO = 'https://seccdn.libravatar.org/avatar/{}?s=256'.format(
    hashlib.md5(email.strip().lower()).hexdigest())
copyright_year_start = 2016
copyright_year_end = datetime.date.today().year
if copyright_year_end == copyright_year_start:
    COPYRIGHT_YEAR = copyright_year_start
else:
    COPYRIGHT_YEAR = '{}-{}'.format(copyright_year_start, copyright_year_end)
PYGMENTS_STYLE = 'native'
```

!!! note

    In the example, I use [libravatar](https://www.libravatar.org/), a
    federated open source avatar hosting service, for my site's logo.
    To use it for your own site, [create an account](
    https://www.libravatar.org/account/new/) with them.

Finally, commit the changes to git:
```
git commit -a -m "Use Flex theme"
```

## Creating a Hello World blog post

To create your first blog post, create a Markdown file in the `content`
directory with the following content:
```
Title: Hello, World!
Date: 2016-10-06 10:52
Category: Site

This is my first blog post using [Pelican](http://blog.getpelican.com/)
and [Flex](https://github.com/alexandrevicenzi/Flex/)!
```

Commit the changes to git with:
```
git add content/
git commit -m "Add Hello World blog post"
```

Preview the site with:
```
fab reserve
```

## Next steps

You have successfully completed setting up a Pelican site. But the site doesn't
really serve its purpose if its only available on your local computer, does it?

I plan to write a follow-up blog post that will show you how to publish your
site to GitHub Pages with a sleek Fabric task to do it automatically. Stay
tuned!

Meanwhile, you can also browse the [source repo of my Pelican site](
https://github.com/tjanez/site).
