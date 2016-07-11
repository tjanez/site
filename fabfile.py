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
