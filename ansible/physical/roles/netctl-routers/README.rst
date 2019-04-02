netctl-routers
==============

Install, configure, start and enable netctl on a router.

Netctl is Arch Linux's home-brew network configuration manager. It's especially
suitable for relatively static hosts, like headless servers. This role does the
following:

1. Install netctl.
2. Install a configuration file for each of the interfaces below. If the
   configuration file is changed in any way, also update the corresponding
   systemd service file. (This includes initial installation.)
3. Start and enable each of the systemd services.

Netctl isn't capable of configuring logical interfaces. Consequently, arguments
should only reference physical interfaces.

Variables:

``netctl_routers_wan_if``
    The name of the WAN network interface.

``netctl_routers_dmz_if``
    The name of the DMZ network interface.

``netctl_routers_lan_if``
    The name of the LAN network interface.

``netctl_routers_wlan_if``
    The name of a WLAN network interface.
