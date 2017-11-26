Title: Enabling updates-testing and epel-testing repositories when using Copr
Date: 2017-11-26 22:13
Category: Fedora
Tags: copr, fedora, epel
Slug: enabling-testing-repos-in-copr

[Copr](https://copr.fedorainfracloud.org) is a really useful [Fedora](
https://getfedora.org/) community build service which also hosts
[dnf](http://dnf.readthedocs.io)/[yum](http://yum.baseurl.org/) repositories of
the built packages.

<!-- PELICAN_BEGIN_SUMMARY -->

When creating a Copr project, one can specify which chroots, i.e. which
distribution version and architecture combinations, to enable. Examples of
chroots are `fedora-27-x86_64`, `epel-7-ppc64le`, `fedora-rawhide-i386` etc.

However, there is no easy to use option to enable testing repositories, e.g.
the [`updates-testing` repository](
https://fedoraproject.org/wiki/Repositories#updates-testing) for Fedora
Branched and stable releases, when specifying the chroots.
Let me show you how you can easily achieve that by specifying an extra
repository with a parameterized URL.

<!-- PELICAN_END_SUMMARY -->

When setting up a Copr project, one can also specify extra repositories to
enable (in the web UI, they are referred to as *External repositories*).

A nice feature of Copr is that the URLs of these extra repositories can be
parameterized with variables representing the name of the distribution
(`$distname`), release version (`$releasever`) and base architecture
(`$basearch`).

Using that, we can easily specify an extra repository that will correspond to
the appropriate testing repository of any given chroot.

Unfortunately, Fedora and [EPEL](https://fedoraproject.org/wiki/EPEL) don't use
the same directory structure, so one can't use the same parameterized extra
repository URL.

If you want to enable the `updates-testing` repository in a Fedora chroot,
add the following extra repository URL to your Copr project:

```
http://download.fedoraproject.org/pub/$distname/linux/updates/testing/$releasever/$basearch/
```

If you want to enable the [`epel-testing` repository](
https://fedoraproject.org/wiki/EPEL/testing) in an EPEL chroot, add the
following extra repository URL to your Copr project:

```
http://download.fedoraproject.org/pub/$distname/testing/$releasever/$basearch/
```

To do this using [Copr command line interface](
https://developer.fedoraproject.org/deployment/copr/copr-cli.html), run the
following:

```bash
copr-cli modify --repo '<parameterized-extra-repository-URL>'
```

For example, to enable the `updates-testing` repository in a Fedora chroot,
run:

```bash
copr-cli modify --repo \
    'http://download.fedoraproject.org/pub/$distname/linux/updates/testing/$releasever/$basearch/'
```

!!! note

    You must put the parameterized extra repository URL in single quotes,
    otherwise Bash will evaluate the variables (e.g. `$distname`) in the
    current context, where they are not defined, and silently substitute them
    with empty strings.

If your Copr project includes a Fedora and an EPEL chroot, just add both,
the `updates-testing` and the `epel-testing` repository, as extra
repositories.

A build of the Copr project in a Fedora chroot will fail to fetch the
information about the (non-existent) `epel-testing` repository, but it will
successfully continue. The same goes for a build in an EPEL chroot or a [Fedora
rawhide](https://fedoraproject.org/wiki/Repositories#The_rawhide_repository)
chroot, which don't have a corresponding `updates-testing` repository.

*[EPEL]: Extra Packages for Enterprise Linux
