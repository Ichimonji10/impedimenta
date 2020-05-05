#!/usr/bin/env bash
# coding=utf-8
#
# Do the following:
#
# * Drop 20% of packets to 8.8.4.4.
# * Delay packets to 8.8.8.8 by 300ms.
# * Allow all other traffic to flow normally.
set -euo pipefail

source exports.sh

# Create a tree of qdiscs and classes.
tc qdisc replace dev "${netif}" root handle 1: htb default 1
for ((minor=1; minor<=3; minor++)); do
    tc class add dev "${netif}" parent 1:0 classid "1:${minor}" htb rate 1mbit ceil 1tbit
done
tc qdisc add dev "${netif}" parent 1:1 fq_codel
tc qdisc add dev "${netif}" parent 1:2 netem loss 20%
tc qdisc add dev "${netif}" parent 1:3 netem delay 300ms

# Direct traffic down the tree.
tc filter add dev "${netif}" parent 1:0 u32 match ip dst 8.8.4.4/32 classid 1:2
tc filter add dev "${netif}" parent 1:0 u32 match ip dst 8.8.8.8/32 classid 1:3
