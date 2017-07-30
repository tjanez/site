Title: Backing up Android's /data/media (i.e. internal storage) using adb and TWRP
Date: 2017-07-30 12:28
Category: Android
Tags: android, backup, twrp, adb, benchmark
Slug: android-internal-storage-backup

<!-- PELICAN_BEGIN_SUMMARY -->

Recently I had to clone my [Nexus 4](https://en.wikipedia.org/wiki/Nexus_4) to
another Nexus 4 device since my Nexus 4's front glass broke :-(.

At first, the task seemed quite straight-forward. Install the latest version of
[TWRP](https://twrp.me/)'s recovery on the phone, backup all partitions using
TWRP, transfer them to the other device and restore them.

But thing are never as easy as them seem, are they?

<!-- PELICAN_END_SUMMARY -->

*[TWRP]: Team Win Recovery Project

## Problems with the straight-forward approach

It turns out that **creating** a **backup of** the **user data partition**
using TWRP **will NOT include `/data/media`** (i.e. your **internal storage**).
That means if you save photos or data on the internal storage (some apps will
save data there as well), they will be not included in a TWRP backup.

This is [explained in TWRP's FAQ](https://twrp.me/faq/backupexclusions.html)
and TWRP's owner also [explained why they exclude `/data/media` from the backup
](https://github.com/TeamWin/Team-Win-Recovery-Project/issues/276#issuecomment-239172861)
in a [heatedly debated GitHub issue on (not) excluding `/data/media` from
TWRP's backups](https://github.com/TeamWin/Team-Win-Recovery-Project/issues/276).

There is even an [old open issue on GitHub](
https://github.com/TeamWin/Team-Win-Recovery-Project/issues/176) that asks for
an implementation of an option to backup `/data/media` using TWRP, but there has
been no updates since Apr 15, 2015 (as of writing this blog post).

## Simple command-line solution using `adb` and `tar`

Browsing the internet for a solution, I found a [nice thread on XDA-developers](
https://forum.xda-developers.com/android/software-hacking/how-to-backup-compressed-data-android-t3464777)
explaining how to backup data from an Android device booted into TWRP to a
computer.

The *trick* is to use [`adb exec-out` command](
https://android.googlesource.com/platform/system/core/+/5d9d434efadf1c535c7fea634d5306e18c68ef1f)
, an undocumented [`adb` command](
https://developer.android.com/studio/command-line/adb.html) that works like
`adb shell` but without creating a pseudoterminal (`pty`), which would
otherwise mangle binary data.

To backup `/data/media` (i.e. internal storage), first reboot your phone into
TWRP recovery.

Then execute the following:

```bash
adb exec-out 'tar --create --exclude=data/media/0/TWRP \
  data/media/0 2>/backup-errors.txt | \
  gzip' | \
dd of=<backup-name>-$(date +%Y%m%d).tar.gz && \
adb shell cat /backup-errors.txt
```

replacing `<backup-name>` with your desired backup name, e.g.
`tadej-nexus4-sdcard_backup`.

## Which compression algorithm to use?

A natural question that comes to mind is, which compression algorithm would
perform best in an overall sense, i.e. with respect to compression ratio and
the time it takes to create and transfer the archive.

Since we are just piping the (compressed) tar archive from the phone to the
computer, we can easily swap between creating the compressed archive on the
phone or on the computer. Compressing the archive on the computer would
not help reducing backup time if the bandwidth is the limit, but it may help
reducing the backup size.
On the other hand, if compression on the phone is CPU-bound, then performing
the compression on the computer will help reduce the backup time.

The variant of the command that compresses files on the computer is:

```bash
adb exec-out 'tar --create --exclude=data/media/0/TWRP \
  data/media/0 2>/backup-errors.txt' | \
<compression-command> | \
dd of=<backup-name>-$(date +%Y%m%d).tar.<compression-extension> && \
adb shell cat /backup-errors.txt
```

where `<compression-command>` is one of `gzip`, `bzip2` and `xz` (optionally,
with extra arguments) and `<compression-extension>` is the chosen compression
tool's extension, i.e. `gz`, `bz2` or `xz`.

The results of backing up my phone's internal storage with different
compression commands and different execution places are the following ([read
more details about the data being backed up in the next section
](#what-kind-of-data-was-being-compressed)):

| Compression command     | Compression execution | Backup size         | Size compared to best  | Backup time | Time compared to best  |
|:----------------------- |:---------------------:| -------------------:| ----------------------:| -----------:| ----------------------:|
| *without*               | *N/A*                 | 3558 MiB            | +4.8%                  | 878 s       | +61%                   |
| `gzip`                  | on the phone          | 3428 MiB            | +1.0%                  | 549 s       | +1%                    |
| `gzip --best`           | on the phone          | 3428 MiB            | +1.0%                  | **545 s**   | *N/A*                  |
| `bzip2`                 | on the phone          | 3411 MiB            | +0.5%                  | 4236 s      | +677%                  |
| `gzip`                  | on the computer       | 3425 MiB            | +0.9%                  | 982 s       | +80%                   |
| `bzip2`                 | on the computer       | 3411 MiB            | +0.5%                  | 824 s       | +51%                   |
| `xz`                    | on the computer       | 3402 MiB            | +0.2%                  | 1566 s      | +187%                  |
| `xz --threads=0`        | on the computer       | 3404 MiB            | +0.3%                  | 811 s       | +48%                   |
| `xz --best --threads=0` | on the computer       | **3395 MiB**        | *N/A*                  | 895 s       | +64%                   |

The **overall winner** is clearly **using `gzip`** and **performing compression
on the phone**. The time needed to perform the backup is the smallest by a
large margin while the backup size is only 1% larger compared to the best
compression achieved with `xz --best`.

!!! note

    Benchmarks were conducted on my Nexus 4 running [TWRP 3.1.1-0
    (twrp-3.1.1-0-mako.img)](https://eu.dl.twrp.me/mako/) connected to my [HP
    ZBook 15 G2 workstation](https://en.wikipedia.org/wiki/HP_ZBook) running
    [Fedora 25 Workstation](https://getfedora.org/en/workstation/).

    [TWRP 3.1.1-0](
    https://twrp.me/site/update/2017/05/19/twrp-3.1.1-0-released.html) is based
    on [OmniROM, a community developed Android derivative](
    https://omnirom.org/), 7.1, which in turn is based on [AOSP](
    https://source.android.com/) 7.1.2.

    TWRP [doesn't use the `gzip` command provided by BusyBox](
    https://github.com/omnirom/android_bootable_recovery/blob/56cf564/Android.mk#L508-L510).
    Rather, it uses the one provided by [`pigz`, a parallel implementation of
    gzip](
    https://github.com/omnirom/android_bootable_recovery/tree/b523650/pigz).
    
    TWRP's [`bzip2` and `xz` commands are provided by Busybox](
    https://github.com/omnirom/android_external_busybox/blob/android-7.1/busybox-full.links#L15).
    Note that [OmniROM still uses Busybox](
    https://github.com/omnirom/android_external_busybox/tree/android-7.1),
    while [AOSP switched to toybox at the end of 2014](
    https://lwn.net/Articles/629362/).

    The `xz` command provided by this version of BusyBox, v1.22.1 bionic,
    doesn't support compression. Note that one can pass the `-J` argument when
    creating an archive with the `tar` command but it will *silently* create an
    uncompressed tar archive.

    Running `xz --best --threads=0` **requires lots of RAM**. More precisely,
    it requires **674 MiB per thread**. For example, on my quad-core CPU with
    hyperthreading enabled, it requires 5.3 GiB of RAM.

*[AOSP]: Android Open Source Project
*[pigz]: Parallel Implementation of GZip

## What kind of data was being compressed?

To be fair and transparent when comparing different compression algorithms, it
is necessary to also tell something about the data being compressed.

The data being compressed is what I accumulated in my phone's user data
partition (i.e. internal storage) over the course of 4 years. Of course, I also
deleted data regularly, otherwise I would run of free space.

This is what makes up the 3558 MiBs of my phone's internal storage:

![My phone's internal storage usage by file type](
{filename}/images/android-internal-storage-backup-usage.svg)

The largest portion is used by JPEG images (mostly pictures taken with the
phone), followed by MP4 videos (also mostly videos taken with the phone),
followed by MPEG and Ogg audio files (my music collection). The rest only
occupies 10 % of the phone's internal storage.
In my opinion, this can serve as a good real-life benchmark of backing up a
phone's internal stoarge.

This also explains why there were so [little differences between different
compression algorithms in the resulting backup size
](#which-compression-algorithm-to-use) (tar archive without compression was
only 4.8 % larger that the smallest tar archive compressed with `xz --best`).
JPEG, MP4, MPEG audio, i.e. MP3, and Ogg Vorbis are all file formats that use
special-purpose compression techniques to reduce the size of files so they
cannot be further compressed to any significant extent.

!!! note

    To analyse my phone's internal storage usage by file type I used
    [lemonsqueeze's `disk_usage_by_file_type` Bash script](
    https://github.com/lemonsqueeze/disk_usage_by_file_type).

    To draw the pie chart, I used [matplotlib](https://matplotlib.org/)
    ([source]({filename}/scripts/android-internal-storage-backup-usage.py)).
