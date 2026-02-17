#!/bin/bash

if [ $# -ne 2 ]; then
    echo "$0 <audio_file> <segments_file>"
    exit 1
fi

audio_file=$(realpath -m $1)
segments_file=$(realpath -m $2)

cd $(dirname $0)

. ./conda-activate.sh

./run_silero_vad.py --audio-file ${audio_file} --segments-file ${segments_file}

