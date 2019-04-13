dns-routers
===========

Configure DNS and DHCP for use in a router.

Configure the target host so that:

*   DHCP service is provided to downstream network clients.
*   DNS service is provided to downstream network clients and local processes.

Configure DNS so that:

*   DNS queries which can't be served from the local cache are forwarded to
    1.1.1.1, or to DHCP-provided DNS servers as a fallback.
*   DNS queries are authenticated with DNSSEC.
*   DNS queries are *not* encrypted. (This would be a great enhancement.)

Variables:

``dnsmasq_lan_if``
    The name of the LAN interface.

``dnsmasq_dmz_if``
    The name of the DMZ interface.

``dnsmasq_secure_wlan_if``
    The name of the secure WLAN interface.
