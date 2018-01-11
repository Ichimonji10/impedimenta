#!/usr/bin/env bash
# coding=utf-8
set -euo pipefail

# Assume this script has been called from the makefile.
source ./bin/common.sh

# See: http://mywiki.wooledge.org/BashFAQ/028
readonly script_name='main.sh'

# Print usage instructions to stdout.
# TODO: Make <output-file> optional. (Print to stdout if not specified.)
show_help() {
fmt <<EOF
Usage: ${script_name} [options] <output-file>

Repeatedly create, populate, publish and delete an RPM repository. Record how
long those steps take, and save those recordings to <output-file>.

Options:
    --iterations <number>
        How many times to create, populate, publish and delete an RPM
        repository. Default: 20.
EOF
}

# Transform $@. $temp is needed. If omitted, non-zero exit codes are ignored.
check_getopt
temp=$(getopt \
    --options '' \
    --longoptions iterations: \
    --name "${script_name}" \
    -- "$@")
eval set -- "${temp}"
unset temp

# Read arguments. (getopt inserts -- even when no arguments are passed.)
if [ "${#@}" -eq 1 ]; then
    show_help
    exit 0
fi
while true; do
    case "$1" in
        --iterations) iterations="${2}"; shift 2;;
        --) shift; break;;
        *) echo "Internal error! Encountered unexpected argument: $1"; exit 1;;
    esac
done
iterations="${iterations:-20}"
if [ -z "${1:-}" ]; then echo >&2 'Missing parameter <output-file>.'; exit 1; fi
output_file="$(realpath "$1")"
shift 1

# Schedule teardown.
teardown() {
    set +e
    if [ -n "${temp_file:-}" ]; then
        rm -f "${temp_file}"
    fi
    pulp-admin rpm repo delete --repo-id src >/dev/null
}
trap teardown EXIT  # bash pseudo signal
trap 'teardown ; trap - SIGINT ; kill -s SIGINT $$' SIGINT
trap 'teardown ; trap - SIGTERM ; kill -s SIGTERM $$' SIGTERM
temp_file="$(mktemp)"

# Do business logic.
pulp-admin login -u admin -p admin >/dev/null
pulp-admin rpm repo create \
    --repo-id src \
    --feed 'https://repos.fedorapeople.org/pulp/pulp/fixtures/rpm-signed/' \
    >/dev/null
pulp-admin rpm repo sync run --repo-id src >/dev/null
for (( i=0; i<iterations; i++ )); do
    ./bin/step.sh >> "${temp_file}"
done

# Copy files to their destination, rather than moving them, to prevent
# teardown() from reaping innocent files.
cp --reflink=auto "${temp_file}" "${output_file}"
