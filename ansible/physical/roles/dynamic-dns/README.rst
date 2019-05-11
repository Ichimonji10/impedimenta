dynamic-dns
===========

Periodically update dynamic DNS service with current IP addressing information.

Install, start and enable several systemd units, where these units periodically
make HTTP GET calls to a given list of URLs.

Variables:

``dynamic_dns_install``
    Whether to install or uninstall scripts. Defaults to true. If false, other
    variables are ignored.

``dynamic_dns_urls``
    A list of URL to periodically make HTTP GET calls to. Each call to a URL
    should be enough to update a dynamic DNS record, assuming a service like
    `FreeDNS`_ is in use. Defaults to an empty list.

.. _FreeDNS: https://freedns.afraid.org/
