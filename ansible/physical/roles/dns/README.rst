dns
===

Configure DNS, and possibly DHCP.

Do the following:

#.  Configure NetworkManager to push changes to ``/etc/resolv.conf`` via
    resolvconf. Only applies to workstations.
#.  Install configure, start and enable dnsmasq. (Dnsmasq provides DHCP and DNS
    service.) Do the following:

    *   Configure dnsmasq to use DNSSEC.
    *   Prepend Cloudflare's privacy-oriented DNS servers to dnsmasq's list of
        name servers. For more on this, see `1.1.1.1`_.

    If the target host is a router, also configure dnsmasq to:

    *   Provide DHCP service to downstream clients.
    *   Provide DNS service to localhost and downstream clients.
    *   Evaulate DNS name servers in order. In other words, favor Cloudflare's
        name servers.

    If the target host is not a router, also configure dnsmasq to:

    *   Do not provide DHCP service.
    *   Provide DNS service to localhost.

#.  Configure the local resolver to use dnsmasq.

Several variables apply to routers:

``dnsmasq_lan_if``
    The name of the LAN interface.

``dnsmasq_dmz_if``
    The name of the DMZ interface.

``dnsmasq_secure_wlan_if``
    The name of the secure WLAN interface.

.. _1.1.1.1: https://1.1.1.1/dns/
