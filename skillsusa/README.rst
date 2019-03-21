SkillsUSA
=========

Code for managing the computers used in the SkillsUSA ITS competition.

Most of the tasks performed by SkillsUSA contestants revolve around Windows
system administration. This presents a challenge: how can the Windows hosts be
reset between each task, so that contestants always work with hosts that are in
a known state? The adopted solution is to use virtual machines. When a
contestant wants to complete a task, preparation consists of the following
steps:

#. Select the appropriate virtual machine(s).
#. Reset the virtual machine(s) to known-good snapshot(s).
#. Start the virtual machine(s).

This presents a new challenge: where will the virtual machines run? Running them
on the computers that contestants use is a bad idea. The computers that
institutions are willing to lend out or donate are frequently low-end: think 2GB
of RAM and a CPU that doesn't support virtualization. The adopted solution is to
run virtual machines on a server or servers.

As per contest rules, all computers are disconnected from the internet. The
computers may be networked together with an unmanaged switch, with a layout like
the following::

    ┌──────────┐     ┌───┐
    │ client-1 ├─────┤ s │
    └──────────┘     │ w │
                     │ i │
    ┌──────────┐     │ t │
    │ client-2 ├─────┤ c │
    └──────────┘     │ h │
                     ╎   ╎
                     ╎   ╎
    ┌──────────┐     │   │
    │ server-1 ├─────┤   │
    └──────────┘     └───┘

Name resolution is performed with the zero-configuration `LLMNR`_ protocol.

The code in this directory helps to manage these hosts. The clients and
server(s) must be connected to the internet while being configured. This is the
recommended use case:

1. Copy the ``bootstrap-client.sh`` script and the key it references onto a
   flash drive.
2. Install Xubuntu onto each client computer. Plug in the flash drive and run
   ``sudo bash bootstrap-client.sh``.
3. Configure virtualization with KVM and Libvirt on the server(s). The process
   for doing this is beyond the scope of this document.
4. Execute the Ansible code to finish configuring the clients and server(s).
   Read the READMEs for each role to learn about the optional variables they
   accept.

.. _LLMNR: https://en.wikipedia.org/wiki/Link-Local_Multicast_Name_Resolution
