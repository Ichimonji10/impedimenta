group-media
===========

Create the ``media`` group.

Certain media files, such as books and movies, don't belong to any one file.
Instead, several applications (such as airsonic) should be able to serve these
files, and a select few users should be able to manually poke at these files.
This role makes this policy possible, with the following procedure:

#.  Create ``/srv/media``.
#.  Ensure new files and directories belong to the ``media`` group.
#.  Ensure new files and directories have ``g+rw`` and ``g+rwx`` permissions,
    respectively.

Users who need management capabilities should depend on this role and be added
to the media group. Hand out access sparingly.

For implementation details, see `setuid`_ and `access control lists`_. For a
higher-level look at how these tools are used, see this forum thread on
`applying default permissions`_.

.. NOTE:: The permission homogenization measures outlined above only fully apply
    to newly created files. Files which are copied or moved from elsewhere may
    belong to a different group or have different permissions.

.. _access control lists: https://wiki.archlinux.org/index.php/Access_Control_Lists
.. _applying default permissions: https://www.linuxquestions.org/questions/linux-desktop-74/applying-default-permissions-for-newly-created-files-within-a-specific-folder-605129/
.. _setuid: https://en.wikipedia.org/wiki/Setuid
