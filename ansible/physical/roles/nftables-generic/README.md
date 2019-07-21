nftables-generic
================

Install and configure nftables.

This role shouldn't be applied to a router.

Example Playbook
----------------

```yaml
- hosts: all:!routers
  roles:
    - nftables
```

The firewall that's installed differs depending on whether the host is in the
following groups:

* bittorrent_hosts
* mnemosyne_hosts
* vm_hosts
* webservers
