libvirtd
========

Create a virtualization environment with libvirt and QEMU.

Additionally:

*   Ensure libvirt can be managed over SSH, with tools such as virt-manager.
*   Install additional CLI tools, such as virt-clone and the libguestfs VM
    customization tools.

For historical reasons, also do the following:

*   Delete several configuration files, scripts, and unit files, including:

    *   ``/usr/local/bin/libvirtd-networking-start``
    *   ``/usr/local/bin/libvirtd-networking-stop``
