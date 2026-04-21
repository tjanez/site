# Tadej Janež's Web site

## Setup Environment

Create a Python virtual environment with Python 3.9:

_NOTE: Old versions of Pelican don't work on the newest Python 3 versions._

```bash
pew new --python python3.9 tadej-site
```

Install these specific versions of Pelican, Fabric and other dependencies:

```bash
pip install \
    pelican==3.7.1 \
    fabric==1.15.0 \
    Jinja2==3.0.3 \
    pymdown-extensions==6.0 \
    markdown==3.0.1
```

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
