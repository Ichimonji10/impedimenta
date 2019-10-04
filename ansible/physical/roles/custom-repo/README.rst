custom-repo
===========

Create and serve repositories of custom packages.

When invoked, this role will do the following:

#. Create a privileged system user dedicated to compiling packages.
#. Install aurutils 2.y.
#. For each repository definition given by the caller:

   #. Create the repository.
   #. Download and compile packages, and place them into the repository.
   #. Configure systemd to automatically update the repository.

The repository and its contents aren't automatically made available. The
repository must be made available through some other means (such as via nginx).
If a repository's contents should be protected (e.g. via an htpasswd file), then
the application which serves the repository is responsible for configuring said
protection.

Sample Playbook
---------------

Sample usage:

.. code-block:: yaml

    - hosts: webservers
      roles:
        - name: custom-repo
          vars:
            custom_repos:
              - path_prefix: /srv/packages.example.com/arch-linux
                name: example-public
                packages:
                  - entr
                  - systemd-boot-pacman-hook
              - path_prefix: /srv/packages.example.com/arch-linux
                name: example-private
                packages:
                  - gog-transistor

Variables
---------

The following variables are accepted:

``custom_repos_user``
    The privileged system user who compiles packages. Not named
    ``custom_repos_packager`` because the term "packager" is closely associated
    with living, breathing human beings who do things like sign off on packages.
    Defaults to ``custom-repo-user``.

    .. WARNING:: The default may change to ``custom-repos-user`` in the future.

``custom_repos_user_home``
    The privileged system user's home directory. Defaults to ``/usr/local/lib/{{
    custom_repos_user }}``.

``custom_repos``
    A list of repository definitions. The following variables may be set in each
    list element:

    ``path_prefix``
        The directory within which the repository will be created. **Must be
        set.** (Sample value: ``/srv/packages.example.com/arch-linux``)

    ``name``
        The name of the repository being created. Consider using a limited set
        of characters for this name, like ``[a-zA-Z-_]+``, as it will be used
        when generating filesystem paths, when generating configuration files,
        and more. **Must be set.** (Sample value: ``custom``)

    ``packages``
        The packages to download, compile, and place in the repository. Defaults
        to an empty list.

    ``auto_update``
        Should the repository's packages automatically be updated when a new AUR
        package is released? Defaults to true.

Discussion
----------

For a recipe for compiling a package to a repository on a once-off basis (as
opposed to through Ansible), see the aur-build(1) man page.

To remove package "foo" from a repository named "custom", execute something like
this:

.. code-block:: sh

    # Remove "foo" from the database listing.
    sudo -u custom-repo-user repo-remove \
        /srv/packages.example.com/arch-linux/custom/custom.db.tar.xz foo

    # Remove "foo" packages from the filesystem.
    rm -f /srv/packages.example.com/arch-linux/custom/foo-*

    # Refresh pacman's database, so it knows about "foo" being removed from
    # "custom."
    pacman -Sy --config /etc/pacman.d/custom.conf

----

Consider the following use case:

    I want to compile AUR packages A and B and add them to a custom repository.
    A (make)depends on B, and B (make)depends on official packages. I don't want
    to locally install A or B. Instead, I want to make them availble to other
    hosts over the network.

How can this be accomplished? Repository management can be done with the
``repo-*`` executables as provided by core/pacman. And B can be compiled with
tools like makechrootpkg(1) as provided by extra/devtools. But there are several
pain points:

* If compiling A, one must start by installing B.
* If A or B are updated on the AUR, then the corresponding local packages won't
  automatically be updated.

aurutils addresses these pain points, though with some twists. The most curious
one is that pacman.conf(5) must contain an entry for each repository being
managed. While the reason is unknown to me, I think this requirement exists for
one the following reason: When compiling A, one of the first steps will be to
install B, and this can only be done if pacman.conf(5) lists a repository that
provides B.

The marriage to pacman.conf(5) creates risk. Imagine that the custom repository
contains a custom version of a package already provided by the official
repositories. In this case, the build server could inadvertently install the
custom package. No solution is currently known, beyond "be careful about what
you package."

One could try working around this issue by creating a custom pacman
configuration file that references the target custom repository, and asking the
various aurutils to use it when compiling packages:

.. code-block:: sh

    #!/usr/bin/env bash
    # coding=utf-8
    set -euo pipefail

    root="$(realpath custom)"
    mkdir "${root}"
    repo-add "${root}/custom.db.tar.xz"

    cp /usr/share/devtools/pacman-extra.conf pacman-custom.conf
    echo '[custom]' >> pacman-custom.conf
    echo 'SigLevel = Optional TrustAll' >> pacman-custom.conf
    echo "Server = file://${root}" >> pacman-custom.conf

    aur sync \
        --chroot \
        --database custom \
        --root "$(realpath custom)" \
        --pacman-conf pacman-custom.conf \
        entr

However, this fails for reasons that are unclear to me. At this time, the best
available solution is "be careful about what you package."

If one does wish to install an AUR package on the build server, it's advisable
to **NOT** list the custom repository as a ``CacheDir`` in pacman.conf(5). Doing
this will save disk space, but a simple ``pacman -Sc`` (or ``-Scc``) can blow
away packages in a cache.

----

Some packages, like `gog-transistor`_, must be served from a private repository
due to copyright issues. This could be done with a playbook roughly like the
following:

.. code-block:: yaml

    # Create, populate and serve custom package repositories.
    - hosts: webservers
      tasks:

      # Compile, locally serve, and install ichi-public/lgogdownloader, and add
      # a gog:// entry to makepkg.conf's DLAGENTS array.
      - include_role:
          name: custom-repo
        vars:
          name: ichi-public
          packages:
            - lgogdownloader
      - name: Install lgogdownloader
        pacman:
          name: lgogdownloader
        become: true
      - include_role:
          name: makepkg-conf

      # Compile and serve packages, including GOG packages, e.g.
      # gog-transistor.
      - include_role:
          name: custom-repo
      - include_role:
          name: nginx

In order to make this playbook work, several implementation issues must be
overcome:

1. How can lgogdownloader authenticate with `GOG`_?

   Ideally, this would be trivial to implement: you would log in to your GOG
   account, get an API token, and then call Ansible with that API token set as a
   variable. In turn, Ansible would have a task which inserts the API token into
   lgogdownloader's configuration file.

   Unfortunately, the semantics of lgogdownloader's configuration files are
   unclear. A simple ``lgogdownloader --login`` produces three different
   configuration files in three different formats, each containing a variety of
   undocumented options, none of which are documented by lgogdownloader(5) or
   ``lgogdownloader --help``.

   While it's tempting to pin the blame on lgogdownloader, its problems may be a
   reflection of GOG's abhorrent API. It includes gems like:

   ``POST /account/tags/update``
       Updates the tag list. Data isn’t actually posted but included as a query
       parameter (wat!?).

   ``GET /account/save_search_privacy/(bool: privacy)``
       Changes if the user can be found by name or email

   ``GET /user/changeLanguage/(str: language)``
       Changes the used locale.

   ``POST /friends/search``
       Search for GOG users.

   Note the inappropriate use of query parameters, the lack of consistency
   between camelCase and snake_case, the inappropriate usage of GET, and the
   inappropriate use of POST. For more, see the unofficial `GOG API
   documentation`_.

   If the abominable API isn't a deal-killer, *and* if security concerns are of
   little import, then then the inability to deploy an API could be worked
   around by making Ansible execute ``lgogdownloader --login`` as the
   ``custom_repo_user`` before calling this role.

   Except that login sometimes fails due to lgogdownloader interacting with an
   HTML page that sometimes contains a reCAPTCHA. ಠ_ಠ
2. How does makepkg know how to download packages from GOG? By adding an entry
   to ``DLAGENTS`` in makepkg.conf(5). What does this new entry look like? Let's
   look at some packages in the AUR:

   * `gog-transistor`_ depends on ``gog://${pkgname//-/_}_${pkgver}.sh``, which
     translates to something like ``gog://gog_transistor_2.0.0.3.sh``.

     I've no idea what official products support the ``gog://`` links. Perhaps
     `GOG galaxy`_?
   * `papers-please-gog`_ depends on
     ``gogdownloader://papers_please/installer_linux_en``.

     The ``gogdownloader://`` links can be consumed by the `GOG downloader`_.
     However, files beginning with this scheme have some limitations (like not
     including version numbers in URLs). In addition, the GOG downloader is no
     longer pushed to users, and I suspect support will be dropped at some
     point.

   This leads to issues like the following

   .. code-block:: sh

       # interactive
       lgogdownloader --login

       # error
       lgogdownloader \
           --download-file 'gogdownloader://papers_please/installer_linux_en'

All of the issues above can be worked around or fixed. But collectively, they
indicate that automatically packaging GOG packages could involve dealing with
bugs, implementing architectural kludges, and researching yet more topics.
Given the small number of games that I'm interested in playing at any given
time, and given how infrequent updates can be, manually packaging them seems
like a better strategy.

Here's a slightly trimmed down example of the concrete commands that could be
used to package gog-pyre:

.. code-block:: sh

    # download
    lgogdownloader --login
    lgogdownloader --list-details --game pyre
    lgogdownloader --download-file 'pyre/en3installer0'

    # package
    aur fetch gog-pyre
    cd gog-pyre
    ln ../pyre_1_50427_11957_23366.sh
    cat PKGBUILD  # read dependencies
    sudo pacman -Sw binkplayer-bin
    makechrootpkg \
        -c \
        -I /var/cache/pacman/pkg/binkplayer-bin-2.7J-1-x86_64.pkg.tar.xz \
        -r /var/lib/archbuild/extra-x86_64/

    # manually add to repo
    sudo install \
        -m 644 \
        -o custom-repo-user \
        -g custom-repo-user \
        gog-pyre-1.50427.11957.23366-1-x86_64.pkg.tar.xz \
        /srv/packages.jerebear.name/arch-linux/ichi-private/
    cd /srv/packages.jerebear.name/arch-linux/ichi-private/
    sudo -u custom-repo-user repo-add ichi-private.db.tar.xz \
        gog-pyre-1.50427.11957.23366-1-x86_64.pkg.tar.xz

.. _gog api documentation: https://gogapidocs.readthedocs.io/en/latest/index.html
.. _gog downloader: https://www.gog.com/downloader
.. _gog galaxy: https://www.gog.com/galaxy
.. _gog-transistor: https://aur.archlinux.org/packages/gog-transistor/
.. _gog: https://www.gog.com/
.. _papers-please-gog: https://aur.archlinux.org/packages/papers-please-gog/
