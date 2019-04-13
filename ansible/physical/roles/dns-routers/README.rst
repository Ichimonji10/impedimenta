dns-routers
===========

Configure DNS and DHCP for use in a router.

Configure the target host so that:

*   DHCP service is provided to downstream network clients.
*   DNS service is provided to downstream network clients and local processes.

Ensure that DNS queries which are forwarded upstream are sent to 1.1.1.1.  These
forwarded queries are not currently protected against tampering with DNSSEC, nor
protected against eavesdropping with encryption.

Variables:

``dnsmasq_lan_if``
    The name of the LAN interface.

``dnsmasq_dmz_if``
    The name of the DMZ interface.

``dnsmasq_secure_wlan_if``
    The name of the secure WLAN interface.
