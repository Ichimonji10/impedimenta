#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

source exports.sh

tc qdisc del dev "${netif}" root
