# Tadej Janež's Web site

My personal web site created with [Pelican].

It uses the [Reflex] theme, a more actively maintained fork of the [Flex] theme.

## Setup Environment

Create a Python virtual environment named `tadej-site`:

```bash
pew new --python python3.13 tadej-site
```

Or using pure Python:

```bash
python3.13 -m venv ~/.local/share/virtualenvs/tadej-site
source ~/.local/share/virtualenvs/tadej-site/bin/activate
```

_NOTE: Using Python 3.14 doesn't work with [Reflex] theme yet._


Install [Pelican], [Fabric] and [PyMdown Extensions]:

```bash
pip install \
    pelican~=4.12 \
    fabric~=1.15 \
    pymdown-extensions~=10.21 \
    minchin.pelican.plugins.summary==1.3.1 \
    pelican-theme-reflex==3.2.0
```

_NOTE: The project's [fabfile.py](fabfile.py) is only compatible with Fabric
1.x._

[Pelican]: https://getpelican.com/
[Reflex]: https://github.com/haplo/pelican-theme-reflex
[Flex]: https://github.com/alexandrevicenzi/Flex
[Fabric]: https://www.fabfile.org/
[PyMdown Extensions]: https://facelessuser.github.io/pymdown-extensions/

## Develop

To generate the site, use:

```bash
fab build
```

To serve the site locally, use:

```bash
fab serve
```

To regenerate the site and serve it locally, use:

```bash
fab reserve
```

## Publish

To generate a clean production version of the site, run:

```bash
fab clean
fab preview
```

To publish the site to GitHub Pages, run:

```bash
fab publish
```
