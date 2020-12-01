#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

persistent_dir='/var/jenkins_home'

docker container stop jenkins
docker container rm jenkins
sudo rm -rf "${persistent_dir}"
