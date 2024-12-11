#!/usr/bin/env bash

BASEDIR="$(dirname $(realpath ${0}))/"
podman run --rm -it --device nvidia.com/gpu=all --security-opt=label=disable \
  -v ${BASEDIR}:/mnt/host_dir:z \
  -v ~/local_data/torch-points3d/change_detection:/mnt/data:z \
  --workdir /mnt/host_dir \
  --entrypoint bash \
  --shm-size 32g \
  ut/torchpoints3d_2:latest
  #localhost/nibio/e2e-oracle-inst-seg:latest
  #docker.io/pytorch/pytorch:2.5.1-cuda12.4-cudnn9-devel
  #principialabs/torch-points3d:latest-gpu


