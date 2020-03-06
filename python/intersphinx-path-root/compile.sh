#!/usr/bin/env bash
# coding=utf-8
#
# TODO: Convert to Python script or make file.
set -euo pipefail

main() {
    declare -ra plugins=(
        intersphinx-path-1
        intersphinx-path-2
    )

    poetry install &
    for plugin in "${plugins[@]}"; do
        get_plugin "${plugin}" &
    done
    wait

    # Build docs twice. In the first pass, indices are created, and in the
    # second pass, those indices are used to create inter-doc links.
    # Consequently, the first pass may be parallel (because we don't depend on
    # indices being present) and the second pass must be serial (because we do
    # depend on indices being present).
    for ((i=0; i<2; i++)); do
        build_root_docs
        for plugin in "${plugins[@]}"; do
            build_plugin_docs "${plugin}"
        done
    done

    # Nicely lay out compiled docs, so that nginx can serve them.
    cp -r docs/_build/html/* collected-docs/
    for plugin in "${plugins[@]}"; do
        cp -r "plugins/${plugin}/docs/_build/html" "collected-docs/plugins/${plugin}"
    done
}

build_plugin_docs() {
    declare -r plugin="$1"
    pushd "plugins/${plugin}/docs/"
    poetry run make clean html
    popd
}

build_root_docs() {
    pushd docs
    poetry run make clean html
    popd
}

# Fetch the target plugin and install its dependencies.
get_plugin() {
    declare -r plugin="${1}"
    # Or `git clone ... plugins/`.
    cp -r "../${plugin}" plugins/
    pushd "plugins/${plugin}"
    poetry install
    popd
}

main
