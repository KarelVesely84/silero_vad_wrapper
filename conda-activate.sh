#!/bin/bash

CONDA_ENV=/mnt/matylda5/iveselyk/VAD_SILERO/CONDA_ENV

# make 'conda activate' findable:
[ -z "${CONDA_EXE}" ] && echo "Error, missing $CONDA_EXE !" && exit 1
CONDA_BASE=$(${CONDA_EXE} info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

# activate the conda environment
conda activate ${CONDA_ENV}

