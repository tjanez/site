from fabric.api import *
import fabric.contrib.project as project
from fabric.contrib.console import confirm
import os
import shutil

# Local path configuration (can be absolute or relative to fabfile)
env.deploy_path = 'output'

# Github Pages configuration
env.github_pages_branch = 'master'

# Port for `serve`
PORT = 8000

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

def gh_pages():
    """Publish to GitHub Pages"""
    main_git_unclean = local('git status --untracked-files=no --porcelain',
                             capture=True)
    if main_git_unclean:
        abort("\n".join(["The main git repository is not clean:",
                         main_git_unclean]))

    clean()
    # build a production version of the site
    preview()

    main_commit_sha = local('git rev-parse --short HEAD', capture=True)
    pages_git_dir = os.path.join(os.path.abspath(env.deploy_path), '.git')
    with lcd(env.deploy_path), shell_env(GIT_DIR=pages_git_dir):
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
