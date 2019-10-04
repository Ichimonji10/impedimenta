nginx
=====

Install, configure and start nginx, and install static website files.

Make the following websites available:

* https://syncthing.jerebear.name
* https://transmission.jerebear.name
* https://www.backtobasicsreading.com
* https://airsonic.jerebear.name
* https://www.jerebear.name

Variables:

* `nginx_ssl_domains`: A list of dicts, where each dict has the following
  keys:

  * domain: The domain for which SSL certificates are being installed, e.g.
    `example.com`.
  * crt: The .crt file to install for this domain.
  * key: The .key file to install for this domain.

* `syncthing_password`: Optional. If omitted, certain tasks are skipped. A
  password to use when setting the htpasswd file for
  https://syncthing.jerebear.name.
* `transmission_password`: Optional. If omitted, certain tasks are skipped. A
  password to use when setting the htpasswd file for
  https://transmission.jerebear.name/downloads/
* `pacman_conf_repo_passwords`: A dict mapping repository names to passwords for
  accessing them. If needed entries are absent, certain tasks are skipped.
