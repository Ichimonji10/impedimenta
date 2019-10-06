dns
===

Configure DNS and/or DHCP.

Effect
------

On workstations:

#.  Configure NetworkManager to push changes to ``/etc/resolv.conf`` via
    resolvconf.
#.  Install configure, start and enable `dnsmasq`_. As a reminder, dnsmasq
    provides DHCP and DNS service. Configure dnsmasq to:

    *   Do not provide DHCP service.
    *   Provide DNS service to localhost.

#.  Configure the resolver to use dnsmasq. As a reminder, the resolver serves
    DNS requests from local processes.

On routers:

#.  Install, configure, start and enable `stubby`_. As a reminder, stubby is a
    DNS stub resolver that supports DNS over TLS. Configure stubby to forward
    queries to a privacy-focused upstream DNS service, namely `1.1.1.1`_.
#.  Install configure, start and enable `dnsmasq`_. As a reminder, dnsmasq
    provides DHCP and DNS service. Configure dnsmasq to:

    *   Forward DNS queries to stubby.
    *   Use DNSSEC.
    *   Provide DHCP service to downstream clients.
    *   Provide DNS service to localhost and downstream clients.

#.  Configure the resolver to use dnsmasq. As a reminder, the resolver serves
    DNS requests from local processes.

This role formerly configured workstations so that dnsmasq would forward
requests to stubby, but this is no longer done. Forwarding requests in this
manner made resolving names on local networks excessively difficult; requests
would never hit the DNS resolver on the local network's router.

Variables
---------

Several variables apply to routers:

``dnsmasq_lan_if``
    The name of the LAN interface. Required.

``dnsmasq_dmz_if``
    The name of the DMZ interface. Required.

``dnsmasq_secure_wlan_if``
    The name of the secure WLAN interface. Required.

.. _1.1.1.1: https://1.1.1.1/dns/
.. _dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _stubby: https://dnsprivacy.org/wiki/display/DP/DNS+Privacy+Daemon+-+Stubby
