# Tadej Janež's Web site

## Setup Environment

Create a Python virtual environment named `tadej-site`:

```bash
pew new tadej-site
```

Or using pure Python:

```bash
python -m venv ~/.local/share/virtualenvs/tadej-site
source ~/.local/share/virtualenvs/tadej-site/bin/activate
```

Install [Pelican], [Fabric] and [PyMdown Extensions]:

```bash
pip install \
    pelican~=4.12 \
    fabric~=1.15 \
    pymdown-extensions~=10.21
```

_NOTE: The project's [fabfile.py](fabfile.py) is only compatible with Fabric
1.x._

[Pelican]: https://getpelican.com/
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
