btrfs-scrub
=============

Periodically scrub a btrfs filesystem.

Let the scrub occur infrequently, such as once a month.

Example Playbook
----------------

.. code-block:: yaml

    - hosts: all
      roles:
        - btrfs-scrub
      vars:
        btrfs_paths:
          - /mnt/btrfs-fs-1
          - /mnt/btrfs-fs-2

Variables
---------

The variables that this role uses, along with their default values, are listed
below.

``btrfs_paths``
    Paths to btrfs mount points, or subdirectories thereof. The entire mounted
    filesystems are scrubbed, regardless of whether mount points or
    subdirectories are specified. Defaults to an empty list.
