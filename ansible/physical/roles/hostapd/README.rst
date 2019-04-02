hostapd
=======

Make a secure wireless network available with hostapd.

Usage
-----

Variables:

``hostapd_secure_if``
    The interface used to advertise the secure network.

``hostapd_secure_name``
    The name of the secure wireless network.

``hostapd_secure_passphrase``
    The passphrase for connective to the secure wireless network.

.. NOTE:: Execute this play only over a wired connection.

Concepts
--------

To learn more about hostapd and related topics, see the following resources:

*   ``/usr/share/doc/hostapd/hostapd.conf``
*   https://en.wikipedia.org/wiki/Service_set_(802.11_network)
*   https://en.wikipedia.org/wiki/List_of_WLAN_channels
*   https://wiki.gentoo.org/wiki/Hostapd
*   ``iw phy``, ``iw dev`` and ``iw dev $ifname link``. ``iw dev <ifname> scan``
    when interface not controlled by hostapd
