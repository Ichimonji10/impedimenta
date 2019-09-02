#!/usr/bin/env bash
# coding=utf-8
#
# Tear down rules which implement split routing based on source IP. This
# script should be called by openvpn's `--route-pre-down` option.
#
set -euo pipefail

ip rule delete table tunnel
ip route flush table tunnel
