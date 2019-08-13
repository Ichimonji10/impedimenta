#!/usr/bin/env bash
# coding=utf-8
#
# Uninstall this app from the current user's home directory.
set -euo pipefail

xdg_data_home="${XDG_DATA_HOME:-${HOME}/.local/share}"

rm -f "${xdg_data_home}/dbus-1/services/name.jerebear.MyService1.service"
rm -f "${xdg_data_home}/dbus-1/services/name.jerebear.KilljoyNotifierNotification1.service"

systemctl --user daemon-reload
