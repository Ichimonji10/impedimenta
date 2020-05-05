#!/usr/bin/env bash
# coding=utf-8
#
# Drop 10% of all egress packets on netif.
set -euo pipefail

source exports.sh

tc qdisc add dev "${netif}" root netem loss 10%
