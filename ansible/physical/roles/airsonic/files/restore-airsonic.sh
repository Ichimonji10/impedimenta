#!/usr/bin/env bash
#
# Restore Airsonic's database. To use, execute as root.
set -euo pipefail

systemctl stop airsonic
install -Dm644 --owner airsonic --group airsonic \
    /var/local/airsonic/backups/airsonic.script \
    /var/lib/airsonic/db/airsonic.script
systemctl start airsonic
