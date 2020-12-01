#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

source common.sh

# Compile website.
#
# If any modifiations are made to the site, then execute `docker container start ${repo}_compiler`.
#
# --volume must be given a full path, or else the site will be malformed. If the contents of the
# source directory change, run this same command again.
docker build --tag jamtur01/jekyll jekyll
if ! [ -d "${repo}" ]; then
    git clone "https://github.com/turnbullpress/${repo}.git"
fi
docker container run \
    --volume "$(realpath "${repo}"):/data/" \
    --name "${repo}_compiler" \
    jamtur01/jekyll

# Serve website.
docker build --tag jamtur01/apache apache
docker container run \
    --detach \
    --publish-all \
    --volumes-from "${repo}_compiler" \
    --name "${repo}_server" \
    jamtur01/apache
docker container port "${repo}_server"
