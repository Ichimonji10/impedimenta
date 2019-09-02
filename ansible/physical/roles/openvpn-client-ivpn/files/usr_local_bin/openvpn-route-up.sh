#!/usr/bin/env bash
# coding=utf-8
# shellcheck disable=SC2154
#
# Configure routing tables to implement split routing based on source IP. This
# script should be called by openvpn's `--route-up` option.
#
set -euo pipefail

ip rule add from "$ifconfig_local" table tunnel
ip route add table tunnel default via "$route_vpn_gateway"
ip route add table tunnel "$route_vpn_gateway" via "$ifconfig_local" dev "$dev"
