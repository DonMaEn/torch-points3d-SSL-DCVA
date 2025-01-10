#!/usr/bin/env bash

# exit on error
set -e

# get podmanfile directory from script location
podmandir=$(dirname $(realpath ${0}))

# tag the podman with 'latest'
tag=ut/torchpoints3d:latest
echo building ${tag}
podman build \
    --tag="${tag}" \
    -v ${podmandir}:/mnt/host_dir:z \
    ${podmandir}
