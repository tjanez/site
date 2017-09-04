Title: Running Fedora 26 on Dell XPS 15 9560
Date: 2017-09-04 9:35
Category: Hardware
Tags: fedora, dell, hardware, laptop
Slug: fedora-26-on-dell-xps-15-9560

<!-- PELICAN_BEGIN_SUMMARY -->

Recently, I got a new laptop, a [Dell XPS 15 9560](
http://www.dell.com/en-us/shop/dell-laptops/xps-15/spd/xps-15-9560-laptop) with
4k display, 32 GiBs of RAM and 1 TiB M.2 SSD drive. Quite nice specs, aren't
they :wink:?

Unfortunately, I wasn't able to purchase it without Windows pre-installed. But
they didn't last long since I wiped the hard drive and installed [Fedora 26](
https://fedoramagazine.org/fedora-26-is-here/) on it.

Let me briefly describe my experience and guide you through some trickier parts
of the setup.

*[SSD]: Solid-state drive

<!-- PELICAN_END_SUMMARY -->

## Configuring UEFI to work with Fedora 26

Before installing Fedora 26 on the system, it is necessary to modify some UEFI
settings. [They are nicely summed up in the ArchWiki page for this laptop](
https://wiki.archlinux.org/index.php/Dell_XPS_15_9560#UEFI):

- Change the *SATA Mode* from the default *RAID* to *AHCI*. This will allow
  Linux to detect the NVMe SSD.
- Change *Fastboot* to *Thorough* in *POST Behaviour*. This will prevent
  intermittent boot failures.

!!! note

    If you intend to run the proprietary NVIDIA graphics drivers, you must also
    disable secure boot.

*[UEFI]: Unified Extensible Firmware Interface
*[NVMe]: Non-volatile memory (NVM) Express

## Booting Fedora 26 from a live USB

The naive approach to just boot the computer from a live USB with Fedora 26
Workstation image and wait for the live [GNOME](https://www.gnome.org/) session
to appear didn't work. Fedora hangs after the *Started User Manager for UID
1000* [systemd unit](
https://www.freedesktop.org/software/systemd/man/systemd.unit.html) starts.

Fortunately, [Ask Fedora has an answer to this problem](
https://ask.fedoraproject.org/en/question/107784/f26-hanging-on-install-dell-xps-9560/?answer=107824#post-id-107824),
which is to select *Troubleshooting* from [GRUB](
https://www.gnu.org/software/grub/)'s boot menu and then choose *Start in basic
graphics mode*. The live GNOME session should work fine after that.

## Installing Fedora 26 to the hard drive

This works smoothly. Just select *Install to Hard Drive* option to start
[Anaconda](https://fedoraproject.org/wiki/Anaconda), Fedora's installer, and
follow its instructions.

After installation, make sure to update all packages to get the latest
kernel (4.12 at the time of writing) and other important updates which will
make Fedora run smoother on this laptop.

## Preventing hangs on boot and soft kernel lockups

The laptop comes with a discrete graphics card, a [NVIDIA GeForce GTX 1050
Mobile(GP107M)](
https://en.wikipedia.org/wiki/GeForce_10_series#GeForce_10_.2810xx.29_series_for_notebooks),
which unfortunately doesn't work well with the [Nouveau drivers](
https://nouveau.freedesktop.org/wiki/) yet (as of kernel 4.12).

!!! note

    Initial support for NVIDIA's GP107 devices [has](
    https://git.kernel.org/linus/b2c4ef70790cee37f243af2b303727394edae1d5)
    [been](
    https://git.kernel.org/linus/2ebd42bc28525da52162425ecd7472846b78584d)
    [merged](
    https://git.kernel.org/linus/5429f82f341524deb9f66193892a69dea2f862a3) into
    kernel 4.12.

Practically, this means that the system will fail to boot (similarly as
[described above](#booting-fedora-26-from-a-live-usb)) if one doesn't disable
Nouveau's power management by passing the `nouveau.runpm=0` parameter to the
kernel at boot. More information in [Red Hat's Bugzilla #1447677](
https://bugzilla.redhat.com/show_bug.cgi?id=1447677).

Unfortunately, that's not enough. After successfully booting the system into
a graphical session, I soon started encountering soft kernel lockups due to
Nouveau driver. The logs showed the following:

```
NMI watchdog: BUG: soft lockup - CPU#1 stuck for 22s! [plymouthd:423]

[ ... output trimmed ... ]

CPU: 1 PID: 423 Comm: plymouthd Not tainted 4.12.9-300.fc26.x86_64 #1
Hardware name: Dell Inc. XPS 15 9560/05FFDN, BIOS 1.3.4 06/08/2017
task: ffff92a115bea640 task.stack: ffffa79943d7c000

[ ... output trimmed ... ]

Call Trace:
 ? nv04_timer_read+0x48/0x60 [nouveau]
 nvkm_timer_read+0xf/0x20 [nouveau]
 nvkm_pmu_reset+0x71/0x170 [nouveau]
 nvkm_pmu_preinit+0x12/0x20 [nouveau]
 nvkm_subdev_preinit+0x34/0x110 [nouveau]
 nvkm_device_init+0x60/0x270 [nouveau]
 nvkm_udevice_init+0x48/0x60 [nouveau]
 nvkm_object_init+0x3f/0x190 [nouveau]
 nvkm_object_init+0xa3/0x190 [nouveau]
 nvkm_client_resume+0xe/0x10 [nouveau]
 nvif_client_resume+0x17/0x20 [nouveau]
 nouveau_do_resume+0x40/0xe0 [nouveau]
 nouveau_pmops_runtime_resume+0x91/0x150 [nouveau]

[ ... output trimmed ... ]

```

Looking through [systemd journal](
https://fedoramagazine.org/systemd-using-journal/) soon revealed other kernel
tracebacks related to the Nouveau driver:

```
nouveau 0000:01:00.0: bus: MMIO read of 00000000 FAULT at 409800 [ TIMEOUT ]
[drm:i915_gem_idle_work_handler [i915]] *ERROR* Timeout waiting for engines to idle
nouveau 0000:01:00.0: timeout
------------[ cut here ]------------
WARNING: CPU: 1 PID: 4100 at drivers/gpu/drm/nouveau/nvkm/engine/gr/gf100.c:1501 gf100_gr_init_ctxctl+0x81f/0x9a0 [nouveau]

[ ... output trimmed ... ]

Hardware name: Dell Inc. XPS 15 9560/05FFDN, BIOS 1.3.4 06/08/2017
task: ffff8d8261e00000 task.stack: ffffa5c91190c000

[ ... output trimmed ... ]

Call Trace:
 gp100_gr_init+0x6f0/0x720 [nouveau]
 gf100_gr_init_+0x55/0x60 [nouveau]
 nvkm_gr_init+0x17/0x20 [nouveau]
 nvkm_engine_init+0x68/0x1f0 [nouveau]
 nvkm_subdev_init+0xb0/0x200 [nouveau]
 nvkm_engine_ref+0x4f/0x70 [nouveau]
 nvkm_ioctl_new+0x2b4/0x300 [nouveau]
 ? nvkm_fifo_chan_dtor+0xe0/0xe0 [nouveau]
 ? gf100_gr_init_fw.isra.8+0x50/0x50 [nouveau]
 nvkm_ioctl+0x118/0x280 [nouveau]
 nvkm_client_ioctl+0x12/0x20 [nouveau]
 nvif_client_ioctl+0x26/0x30 [nouveau]
 usif_ioctl+0x637/0x750 [nouveau]
 nouveau_drm_ioctl+0xaf/0xc0 [nouveau]

[ ... output trimmed ... ]

---[ end trace 1ee905135b51d0af ]---
nouveau 0000:01:00.0: gr: init failed, -16
nouveau 0000:01:00.0: timeout
------------[ cut here ]------------
WARNING: CPU: 2 PID: 4100 at drivers/gpu/drm/nouveau/nvkm/subdev/mmu/gf100.c:190 gf100_vm_flush+0x1ab/0x1c0 [nouveau]

[ ... output trimmed ... ]

Hardware name: Dell Inc. XPS 15 9560/05FFDN, BIOS 1.3.4 06/08/2017
task: ffff8d8261e00000 task.stack: ffffa5c91190c000

[ ... output trimmed ... ]

Call Trace:
 nvkm_vm_unmap_at+0xbc/0x100 [nouveau]
 nvkm_vm_unmap+0x1b/0x20 [nouveau]
 nouveau_gem_object_close+0x1aa/0x1c0 [nouveau]
 drm_gem_object_release_handle+0x4b/0x90 [drm]
 drm_gem_handle_delete+0x58/0x80 [drm]
 drm_gem_close_ioctl+0x20/0x30 [drm]
 drm_ioctl+0x213/0x4d0 [drm]
 ? drm_gem_handle_create+0x40/0x40 [drm]
 ? sock_write_iter+0x8c/0xf0
 nouveau_drm_ioctl+0x72/0xc0 [nouveau]
---[ end trace 1ee905135b51d0b0 ]---
```

Rhys Kidd, a Nouveau developer, wrote the following in [an answer to a bug
report for a similar issue on freedesktop.org's Bugzilla](
https://bugs.freedesktop.org/show_bug.cgi?id=102275#c1) on Aug 17, 2017:

> Nouveau has difficulties with the GTX 1050 Mobile (GP107/NV137) around power
> state up/down. I'd suggest you continue to follow [that bug report](
> https://bugs.freedesktop.org/show_bug.cgi?id=100228) for further updates.

> Whilst `nouveau.runpm=0` assists a little bit, for now, to improve the
> experience on the XPS 9560 you should use `nouveau.modeset=0` (although that
> does mean the Nvidia GPU is unavailable for use). This suggestion might
> change with future kernel releases.

To follow his suggestion and permanently add `nouveau.modeset=0` to the
kernel's command line options, edit `/etc/default/grub` and append
`nouveau.modeset=0` to the contents of the `GRUB_CMDLINE_LINUX` variable.

Afterwards, run `sudo grub2-mkconfig -o /etc/grub2-efi.cfg` to regenerate
GRUB's configuration.

## Updating firmware to version 1.3.4+

It is important to upgrade the laptop's firmware to (at least) [version 1.3.4](
https://www.notebookcheck.net/XPS-15-9560-gets-BIOS-update-fixing-Skylake-Kaby-Lake-microcode-bug.232054.0.html)
since it fixes [a serious issue with Intel's Skylake and Kaby Lake
architectures where the CPU could dangerously misbehave when hyper-threading is
enabled](https://lwn.net/Articles/726496/).

Fortunately, Dell has put Linux users in the prime seat and offers seamless
firmware updates on Linux via [Richard Hughes](
https://blogs.gnome.org/hughsie/)'s excellent [fwupd tool](
http://www.fwupd.org/).

To update the firmware using command line, simply run:

```bash
fwupdmgr refresh
fwupdmgr get-updates
```

to see the list of available updates. To download the available update and
install it after reboot, run:

```bash
fwupdmgr update
```

Alternatively, you can also update the firmware using GNOME's [Software app](
https://wiki.gnome.org/Apps/Software).

# Issues with wireless performance on kernel 4.12

I've experienced [an order of magnitude wireless performance drop after
upgrading from `kernel-4.11.11-300.fc26.x86_64` to `kernel-4.12.5-300.fc26`](
https://bodhi.fedoraproject.org/updates/kernel-4.12.5-300.fc26#comment-645648)
with the Qualcomm Atheros QCA6174 802.11ac wireless network adapter that is
installed in the laptop.
The reported wireless link speed is in 1 - 6 Mbps range, which is very low.

I haven't had time to investigate this further yet.

# Conclusion

Overall, my experience (minus the problems with NVIDIA's graphics card and
its open-source drivers and the wireless performance issue) has been quite
positive.

Sadly, getting all the features of a new laptop to work seamlessly after it
launches is *not there yet* and one still has to be quite knowledgable to make
the most out of the system.

However, I'm optimistic and I think it's getting better. For example, I was
pleasantly surprised how GNOME seamlessly re-scales the interface after
connecting/disconnecting a non-HiDPI monitor. Suspend also works without a
hitch!
