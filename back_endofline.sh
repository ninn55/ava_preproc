#!/bin/bash
# The front line.
# Contains generation of key frames clips

#annot_file
annotfile="./preproc_fallDown/ava_v1.0_extend_annot.csv"
#json_file
jsonfile="./demo/demo_out.json"
#actionlist_file
actionlistfile="./preproc_fallDown/ava_action_list_v2.0.csv"
#output_dir
outputdir="./preproc_fallDown"

echo "Generating keyframes."
python3 ./scripts/parsejson.py --annot_file $annotfile --json_file $jsonfile
echo "Generating clips."
python3 ./scripts/drawbbox.py --annot_file $annotfile --actionlist_file $actionlistfile --output_dir $outputdir