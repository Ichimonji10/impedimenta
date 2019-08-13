#!/usr/bin/env bash
# coding=utf-8
#
# Install this app into the current user's home directory.
set -euo pipefail

xdg_data_home="${XDG_DATA_HOME:-${HOME}/.local/share}"

install -Dm644 \
  -t "${xdg_data_home}/dbus-1/services" \
  "files/name.jerebear.MyService1.service"
install -Dm644 \
  -t "${xdg_data_home}/systemd/user" \
  "files/my-service.service"

systemctl --user daemon-reload
