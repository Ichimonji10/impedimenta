transmission
============

Install, configure, start and enable Transmission bittorrent client.

When executed, this role will do the following:

1. Install transmission.
2. Install a script that Transmission executes when it starts up. This script
   does the following:

   1. Wait for a VPN tunnel to become available and be initialized with an IPv4
      address.
   2. If Transmission doesn't have a configuration file, create one. Otherwise,
      set several parameters in it. These parameters include the tunnel IP
      address and speed limits.

3. Install an override file for transmission.service. This override file ensures
   that a tunnel is available when transmission.service is running, and it
   ensures that the aforementioned script executes before transmission.service
   starts.
4. Start and enable Transmission.

Variables
---------

``transmission_password``
    A password that users must provide to Transmission to view its web
    interface. If provided, the Transmission configuration script is installed.
    Also used by the nginx role. Optional, but if omitted, certain tasks will be
    skipped.
