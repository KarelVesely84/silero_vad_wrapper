#!/bin/bash
exit 0  # intended for copy-pasting lines to shell

# create conda env

ROOT_PATH=${PWD}

conda create --prefix ${ROOT_PATH}/CONDA_ENV python=3.11

conda activate ${ROOT_PATH}/CONDA_ENV

conda update -n base -c defaults conda


pip install ipdb ipython matplotlib
# Dependencies: pure-eval, ptyprocess, wcwidth, traitlets, six, pyparsing, pygments, pillow, pexpect, parso, kiwisolver, fonttools, executing, decorator, cycler, contourpy, asttokens, stack_data, python-dateutil, prompt_toolkit, matplotlib-inline, jedi, ipython-pygments-lexers, matplotlib, ipython, ipdb

pip install silero_vad
# Dependencies: nvidia-cusparselt-cu12, mpmath, flatbuffers, typing-extensions, triton, sympy, protobuf, nvidia-nvtx-cu12, nvidia-nvshmem-cu12, nvidia-nvjitlink-cu12, nvidia-nccl-cu12, nvidia-curand-cu12, nvidia-cufile-cu12, nvidia-cuda-runtime-cu12, nvidia-cuda-nvrtc-cu12, nvidia-cuda-cupti-cu12, nvidia-cublas-cu12, numpy, networkx, MarkupSafe, fsspec, filelock, cuda-pathfinder, onnxruntime, nvidia-cusparse-cu12, nvidia-cufft-cu12, nvidia-cudnn-cu12, jinja2, cuda-bindings, nvidia-cusolver-cu12, torch, torchaudio, silero_vad

pip install torchcodec  # dep. of torchaudio 2.10.0+cu128
pip install pandas  # dep. of `silero_vad/utils_vad.py` in make_visualization
