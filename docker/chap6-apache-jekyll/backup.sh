#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

source common.sh

docker run \
    --rm \
    --volumes-from "${repo}_compiler" \
    --volume "$(realpath .):/backup" \
    ubuntu tar cvf "/backup/${repo}_backup.tar" /var/www/html
