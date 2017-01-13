Title: Don't mix yum/dnf and pip for installation of system-wide Python packages
Date: 2017-01-13 11:43
Category: Python
Tags: yum, dnf, pip, python, packaging, virtualenv, fedora, centos, rhel
Slug: dont-mix-yum-dnf-and-pip

Too many times I've seen people using a mix of [yum](http://yum.baseurl.org/)/
[dnf](http://dnf.baseurl.org/) and [pip](https://pip.pypa.io/) for
installation of system-wide Python packages This causes [all sorts of problems
]({filename}dont-mix-yum-dnf-and-pip.md#problems-with-mixing-yumdnf-and-pip).

**TL; DR** *Install system-wide Python packages with yum/dnf and only use pip
inside a [virtual environment](https://virtualenv.pypa.io/). For an example,
see my [Ansible snippet below
]({filename}dont-mix-yum-dnf-and-pip.md#ansible-playbook-for-installation-of-packages-inside-a-virtual-environment).*

<!-- PELICAN_END_SUMMARY -->

!!! note

    I'll use [CentOS](https://www.centos.org/) 7 for the examples, but the
    concepts apply to all current [Fedora](https://getfedora.org/) and
    CentOS/[RHEL](
    https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux)
    distributions.


## Problems with mixing yum/dnf and pip

People usually install the `python2-pip` package to boot-strap installation of
pip on their systems:

```
sudo yum -y install epel-release
sudo yum -y install python2-pip
```

At the time of writing, this will install pip 8.1.2 on the system, while the
latest pip version is 9.0.1.
A user will soon notice that on each run of the `pip` command the following
message is shown:

```
You are using pip version 8.1.2, however version 9.0.1 is available.
You should consider upgrading via the 'pip install --upgrade pip' command.
```

Naively, he will upgrade pip with:

```
sudo pip install --upgrade pip
```

which will replace the previous pip installation in system locations (e.g.
`/usr/bin`, `/usr/lib/python2.7/site-packages/pip`, ...) with the new pip
version.

The problem is that this will leave [RPM](http://rpm.org/) with no clue as to
what is going on. If you run `rpm --verify python2-pip` it will show that
everything is broken:

```bash
S.5....T.    /usr/bin/pip
S.5....T.    /usr/bin/pip2
S.5....T.    /usr/bin/pip2.7
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info/PKG-INFO
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info/SOURCES.txt
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info/dependency_links.txt
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info/entry_points.txt
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info/not-zip-safe
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info/requires.txt
missing     /usr/lib/python2.7/site-packages/pip-8.1.2-py2.7.egg-info/top_level.txt
S.5....T.    /usr/lib/python2.7/site-packages/pip/__init__.py
S.5....T.    /usr/lib/python2.7/site-packages/pip/__init__.pyc
missing     /usr/lib/python2.7/site-packages/pip/__init__.pyo
.......T.    /usr/lib/python2.7/site-packages/pip/__main__.py
S.5....T.    /usr/lib/python2.7/site-packages/pip/__main__.pyc
missing     /usr/lib/python2.7/site-packages/pip/__main__.pyo

[ ... output trimmed ... ]

S.5....T.    /usr/lib/python2.7/site-packages/pip/vcs/subversion.py
S.5....T.    /usr/lib/python2.7/site-packages/pip/vcs/subversion.pyc
missing     /usr/lib/python2.7/site-packages/pip/vcs/subversion.pyo
S.5....T.    /usr/lib/python2.7/site-packages/pip/wheel.py
S.5....T.    /usr/lib/python2.7/site-packages/pip/wheel.pyc
missing     /usr/lib/python2.7/site-packages/pip/wheel.pyo
```

Furthermore, when a new version of the `python2-pip` becomes available, yum
upgrade will complain about not being able to find some files and directories.

For example, on upgrade from `python-pip-7.1.0-1.el7` to
`python2-pip-8.1.2-5.el7` when pip was upgraded with pip in-between, yum
upgrade gives the following warnings:

```bash
warning: file /usr/lib/python2.7/site-packages/pip/_vendor/_markerlib/markers.pyo: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip/_vendor/_markerlib/markers.pyc: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip/_vendor/_markerlib/markers.py: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip/_vendor/_markerlib/__init__.pyo: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip/_vendor/_markerlib/__init__.pyc: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip/_vendor/_markerlib/__init__.py: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip/_vendor/_markerlib: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/top_level.txt: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/requires.txt: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/pbr.json: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/not-zip-safe: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/entry_points.txt: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/dependency_links.txt: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/SOURCES.txt: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info/PKG-INFO: remove failed: No such file or directory
warning: file /usr/lib/python2.7/site-packages/pip-7.1.0-py2.7.egg-info: remove failed: No such file or directory
```


## Proper way to to use pip without mixing it with yum/dnf

The solution is to limit pip's use to installation of Python packages inside a
Python virtual environment.

First install the `python-virtualenv` package with yum/dnf:

```
sudo yum -y install python-virtualenv
```

Then use it to create and activate a new virtual environment:

```
virtualenv myvenv
source myvenv/bin/activate
```

!!! note

    At the time of writing, CentOS 7's system-installed virtualenv package is
    very old (1.10.1) and creates a virtual environment with very old pip
    (1.4.1) and setuptools (0.9.8) packages. Hence, it is recommended to update
    them separately, before installation of other things in the virtual
    environment with:

        pip install -U pip setuptools

Then install whichever Python package you want inside the Python virtual
environment.

### Tip: Don't install the system pip package

To avoid mistakenly using pip outside a virtual environment, don't install
the pip system package (e.g. `python2-pip`).

This way, `pip` executable will only be available after you activate the chosen
virtual environment, which limits mistakes with using the system-wide pip to
the minimum.

## Ansible playbook for installation of packages inside a virtual environment

If you need to automate installation of `python-virtualenv` system package and
creation of a Python virtual environment for installation of project's
requirements inside this virtual environment, you can use the following
[Ansible](https://www.ansible.com/) playbook:

```yaml
- name: Playbook for installation of packages inside a virtual environment
  hosts: all
  become: true

  vars:
    # adjust these variables to your project's needs
    venv_path: /opt/myvenv/
    requirements:
      - requests
      - simplejson
      - six

  tasks:
    - name: Install python-virtualenv package
      package: name=python-virtualenv state=installed

    - name: Create virtual environment with up-to-date pip and setuptools
      pip:
        virtualenv: "{{ venv_path }}"
        name:
          - pip
          - setuptools
        state: latest

    - name: Install project's requirements in virtual environement
      pip:
        virtualenv: "{{ venv_path }}"
        name: "{{ requirements }}"
        state: latest
```

!!! note

    Due to a [bug in Ansible's `pip` module](
    https://github.com/ansible/ansible-modules-core/issues/5347) which causes
    Ansible to use system-installed `pip2` executable and ignore the `pip`
    executable installed inside the virtual environment, you must use at least
    [version 2.2.1 RC3](
    https://releases.ansible.com/ansible/ansible-2.2.1.0-0.3.rc3.tar.gz) which
    fixes the bug.

If your project's requirements are not pure Python packages, but also include
packages with [C/C++ extensions](
https://docs.python.org/3/extending/index.html), they'll need to be built as
part of the installation process. Therefore, you'll need to have at least `gcc`
and `python-devel` packages installed. You can use the following Ansible task
to achieve that:

```yaml
    - name: Install project's building prerequisites
      package: name={{ item }} state=installed
      with_items:
        - gcc
        - python-devel
        # add other packages required to build your project's requirements
```

Put it before the *Install project's requirements in virtual environement*
task.
