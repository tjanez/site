Title: Publishing a Pelican site to GitHub Pages using Fabric
Date: 2016-10-19 19:05
Category: Site
Tags: pelican, python, fabric, github, site
Slug: publishing-to-github-pages

*Update (May 25, 2018): Starting with May 1, 2018, [GitHub Pages gained support
for serving custom domains over HTTPS](https://blog.github.com/2018-05-01-github-pages-custom-domains-https/).
I've updated the [Setting up a custom domain](#setting-up-a-custom-domain)
section of this blog post to advise users to use this functionality.*

<!-- PELICAN_BEGIN_SUMMARY -->

In the [previous blog post]({filename}setting-up-pelican-site.md) we looked at
setting up a [Pelican](http://getpelican.com/) site with [Python 3](
https://www.python.org/) and [Fabric](http://www.fabfile.org/) on [Fedora 24](
https://getfedora.org/).

Now that we have a Pelican site up and running, I will show you how to publish
it on [GitHub Pages](https://pages.github.com/) using a sleek Fabric task.

<!-- PELICAN_END_SUMMARY -->

## Review of existing approaches

There are various approaches to managing publishing your Pelican site to
GitHub Pages.

[Pelican authors recommend](
http://docs.getpelican.com/en/stable/tips.html#publishing-to-github) using the
[`ghp-import` tool](https://github.com/davisp/ghp-import) to import the
contents of the `output` directory to a special `gh-pages` git branch, which
can then be pushed to the desired GitHub pages repository's branch (i.e.
`master` branch for User pages or `gh-pages` branch for Project pages).

[Ankur Sinha](http://ankursinha.in/blog/) wrote an
[excellent article for Fedora Magazine](
https://fedoramagazine.org/make-github-pages-blog-with-pelican/), where he
recommends creating two git repositories, the main repository containing the
source of the Pelican page and the second repository containing the contents of
the `output` directory.
The recommendation is to add the second repository as a submodule of the main
repository.

I didn't find any of those two approaches satisfy my needs.
The downside of using the `ghp-import` tool is that it is not packaged for
Fedora yet ([review request](
https://bugzilla.redhat.com/show_bug.cgi?id=1183422)) and that it destroys the
`gh-pages` branch on each run, thus one is unable to keep previous contents of
the page as older commits.
On the other hand, tracking the contents of the `output` directory as a
submodule in a separate git repo has the disadvantage of having to update the
submodule reference in the main git repo every time a new version of the site
is built, thus leading to a large number of "submodule bump" commits in the
main git repo.

## A new approach using a custom Fabric task

Therefore, I crafted a new approach that tries to overcome these disadvantages.
Like in Ankur Sinha's article, I created two git repositories, the main
repository containing the source of the Pelican page and the second repository
containing the contents of the `output` directory.
However, instead of linking the repositories via a submodule, I just created
a custom Fabric task that rebuilds the source page, commits its output to the
second git repository and pushes it to GitHub Pages.

To use this approach, first create the *username*.github.io repository on
[GitHub](https://github.com/new).

Then generate a clean production version of the site:

```
fab clean
fab preview
```

Add the contents of the `output` directory to the *username*.github.io git
repository:

```
cd output
git init
git add --all
git commit -m "Initial commit"
git remote add origin git@github.com:<username>/<username>.github.io.git
git push origin master
```

Edit `publishconf.py` and remove the following line:

```python
DELETE_OUTPUT_DIRECTORY = True
```

This will prevent Pelican from deleting the whole `output` directory, including
the git repository initialized in the previous step, when building the
production version of the site.

Modify the `clean` function in Fabric's `fabfile.py` to not delete the `.git`
directory:

```python
def clean():
    """Remove generated files"""
    for root, dirs, files in os.walk(env.deploy_path):
        for name in dirs[:]:
            # Do not recurse into this directory
            dirs.remove(name)
            if name == '.git':
                # Do not remove .git/ directory
                pass
            else:
                shutil.rmtree(os.path.join(root, name))
        for name in files:
            os.remove(os.path.join(root, name))
```

Add the following `gh_pages` function (and its `publish` alias) to Fabric's
`fabfile.py`:

```python
from fabric.contrib.console import confirm

# Get absolute path of project's root directory
env.project_root = os.path.dirname(env.real_fabfile)
# Set absolute path of project's deploy directory
env.deploy_path = os.path.join(env.project_root, 'output')

# Github Pages configuration
env.github_pages_branch = 'master'

def gh_pages():
    """Publish to GitHub Pages"""
    with lcd(env.project_root):
        # ensure the main git repository is clean
        main_git_unclean = local('git status --untracked-files=no --porcelain',
                                 capture=True)
        if main_git_unclean:
            abort("\n".join(["The main git repository is not clean:",
                             main_git_unclean]))
        # get main git repository's HEAD's sha checksum
        main_commit_sha = local('git rev-parse --short HEAD', capture=True)

    with lcd(env.deploy_path):
        # sync local GitHub Pages git repository with remote repository
        local('git fetch origin {github_pages_branch}'.format(**env))
        local('git reset --hard origin/{github_pages_branch}'.format(**env))

    clean()
    # build a production version of the site
    preview()

    with lcd(env.deploy_path):
        pages_git_unclean = local('git status --porcelain', capture=True)
        if pages_git_unclean:
            local('git add --all')
            local('git commit -m "Build of source repo @ {}"'.format(main_commit_sha))
            if confirm("Do you wish to publish the current version of the "
                       "page to GitHub Pages?", default=False):
                local('git push origin {github_pages_branch}'.format(**env))
                commit_sha = local('git rev-parse --short HEAD', capture=True)
                puts("Pushed commit {} to GitHub Pages".format(commit_sha))
            else:
                # reset the git repo to the one on GitHub Pages
                local('git reset origin/master')
                puts("Exiting on user request.")
        else:
            puts("Nothing has changed. Exiting.")

def publish():
    """Publish to GitHub Pages"""
    gh_pages()
```

To publish the page, run:

```
fab publish
```

and answer `y` when prompted.

Visit the page at https://*username*.github.io and share it with the World!

## Setting up a custom domain

To use a custom domain with GitHub Pages, e.g. `blog.mysite.com`, one needs to
add a `CNAME` file in the root of the generated site which tells GitHub Pages
on which custom domain the site is hosted.

The contents of the file should match the custom domain name. For the example
custom domain above, one would create the file `content/extra/CNAME` with
the following content:

```
blog.mysite.com
```

To instruct Pelican to copy the `CNAME` file to site's root, list it among
site's static paths:

```python
STATIC_PATHS = [
    ... other static paths ...
    # GitHub Pages custom domain
    'extra/CNAME',
]
```

and annotate it with extra path metadata:

```python
EXTRA_PATH_METADATA = {
    ... other extra path metadata ...
    'extra/CNAME': {'path': 'CNAME'},
}
```

Finally, change the value of `SITEURL` variable in `publishconf.py` to the
custom domain's name and commit the changes:

```
git add content/extra/CNAME
git commit -a -m "Change site's URL to https://blog.mysite.com"
```

Before we publish the new version of the site with a custom domain, we need
to configure an appropriate DNS record with our DNS provider. The above example
custom domain is a custom **subdomain**, so we need to set up a `CNAME` record
with our DNS provider that points to *username*.github.io. Follow your DNS
provider's instructions on how to do that.

To confirm that the new DNS record is set up correctly, use the `dig` utility:

```
dig +nocmd +nostats +nocomments blog.mysite.com
```

and make sure the output is similar to:

```
;blog.mysite.com.               IN  A
blog.mysite.com.        1747    IN  CNAME   username.github.io.
username.github.io.     3547    IN  CNAME   github.map.fastly.net.
github.map.fastly.net.  650     IN  CNAME   prod.github.map.fastlylb.net.
prod.github.map.fastlylb.net. 17 IN A       151.101.12.133
```

If your custom domain is an apex domain (e.g. `mysite.com`), you will need
to configure a different type of a DNS record. See [GitHub Pages's Help on
Setting up an apex domain](
https://help.github.com/articles/setting-up-an-apex-domain/).

After DNS is properly configured, publish the updated site to GitHub Pages
with:

```
fab publish
```

Visit the page at your custom domain!

!!! note

    Starting with May 1, 2018, [GitHub Pages gained support for serving custom
    domains over HTTPS](https://blog.github.com/2018-05-01-github-pages-custom-domains-https/).

    You are advised to take advantage of this functionality and server your
    site over HTTPS. If you've used a `CNAME` record with your DNS provider,
    then you should be all set.

    After ensuring your site loads correctly over HTTPS, browse to
    https://github.com/*username*/*username*.github.io/settings and
    enable the *Enforce HTTPS* option under the *GitHub Pages* section. This
    will transparently redirect any HTTP requests to your site to HTTPS.

To see this implemented in practice, browse the
[source repo of my Pelican site](https://github.com/tjanez/site/tree/5012f31).
