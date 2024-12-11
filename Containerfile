from docker.io/pytorch/pytorch:1.9.1-cuda11.1-cudnn8-devel

RUN apt update \
||  apt install -y libusb-1.0-0 libgl1

#RUN conda install \
#    wandb \
#    hydra-core \
#
#RUN conda install -c torch-points3d torch-points-kernels
#
#RUN conda install pyg -c pyg

RUN conda install numba

ENV TORCH_CUDA_ARCH_LIST="8.0"
ENV FORCE_CUDA=1
RUN pip install scikit-learn && \ 
    pip install --no-deps \
    torch-points-kernels

RUN pip install \
    torch_scatter==2.0.8 -f https://data.pyg.org/whl/torch-1.10.0+cu111.html \
    torch_cluster==1.5.9 -f https://data.pyg.org/whl/torch-1.10.0+cu111.html \
    torch_sparse==0.6.12 -f https://data.pyg.org/whl/torch-1.10.0+cu111.html

#RUN pip install --upgrade pip \
RUN pip install \
    hydra-core==1.0.7 \
    wandb==0.8.36 \
    torch_geometric==1.7.2 \
    scikit-learn \
    torchnet==0.0.4 \
    h5py==3.4.0 \
    pandas==1.1.5 \
    gdown==3.13.1 \
    tensorboard==2.6.0 \
    plyfile==0.7.4 \
    pytorch-metric-learning==0.9.99 \
    imageio==2.9.0 \
    scikit-image==0.16.2 \
    open3d==0.12.0 \
    laspy==2.0.3 \
    pycuda \
    matplotlib==3.4.3 \
    protobuf==3.18.0

