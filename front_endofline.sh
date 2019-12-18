#!/bin/bash
# The front line.
# Contains generation of key frames clips

#video_dir
videodir="./vid_fallDown"
#output_dir
outputdir="./preproc_fallDown"

echo "Generating keyframes."
python3 ./scripts/genkeyframe.py --video_dir $videodir --output_dir $outputdir
echo "Generating clips."
python3 ./scripts/genclip.py --video_dir $videodir --output_dir $outputdir