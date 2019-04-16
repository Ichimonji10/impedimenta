dns-generic
===========

Configure DNS on a non-router host.

Do the following:

*   Configure NetworkManager to push changes to ``/etc/resolv.conf`` via
    resolvconf. Only applies to hosts that have NetworkManager installed.
*   Configure dnsmasq to serve local DNS requests, enforce DNSSEC, and use
    1.1.1.1 as one of the upstream DNS resolvers.
*   Configure the local resolver to use dnsmasq.
