borg-backup-system
==================

Configure system-wide backups with `Borg`_.

More specifically, do the following:

1. Install borg.
2. Create a system user that will perform backups, and ensure this user belongs
   to the "root" group.
3. Install ``~/.ssh/borg-backup`` and ``~/.ssh/config`` for this user.
4. Install a system-wide script to perform backups, and ensure only the backup
   user can run it.
5. Install, start and enable system-wide units to periodically call the backup
   script.

The Borg repositories on the remote backup host are distinguished by host names.
As a result, multiple hosts may back up to the same remote backup host.

Example playbook:

.. code-block:: yaml

    - hosts: all
      roles:
        - borg-backup-system
      vars:
        borg_backup_system_local_paths:
          - /var/local/airsonic/backups
        borg_backup_system_passphrase: pass
        borg_backup_system_private_key: /path/to/key

Variables:

``borg_backup_system_local_paths``
    Required. A list of paths to back up. These paths are subject to Bash's
    expansion rules. If the paths contain whitespace or other interesting
    characters, consider using single quotes.

``borg_backup_system_local_user``
    Optional. The username of the local user that will perform system-wide Borg
    backups.

``borg_backup_system_local_user_home``
    Optional. The home directory for ``borg_backup_system_local_user``.

``borg_backup_system_passphrase``
    Optional, but some tasks are skipped if omitted. The passphrase needed to
    decrypt the remote Borg repository.

``borg_backup_system_private_key``
    Optional, but some tasks are skipped if omitted. The path to a private SSH
    key that will be used when SSHing to the remote host that hosts the Borg
    repository.

``borg_backup_system_remote_host``
    Optional, but some tasks are skipped if omitted. The hostname of the host
    which will host Borg backups.

``borg_backup_system_remote_user``
    Optional, but some tasks are skipped if omitted. The username on the remote
    host who will host Borg backups.

.. _Borg: https://borgbackup.readthedocs.io/en/stable/
