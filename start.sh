#!/bin/bash
# Generate the segmentation mask and classif-
# ication dataset for a given images.

if [ $# -eq 0 ]
then
    echo "Please specify the datapath"
    elif [ $# -gt 1 ]
    then
        echo "You provided more than one filepath"
        echo "Example sh start.sh path/to/data"
fi
if [ $# -eq 1 ]
then
    img_len=$(find $1 -type f -depth 1 -name "*.jpg" | wc -l)
    json_len=$(find $1 -type f -depth 1 -name "*.json" | wc -l)

    printf "Found %d images in %s\n" $img_len $1
    printf "Found %d json files in %s\n" $json_len $1
    echo
    echo "Starting ...."

    $(python3 mask_from_annotation.py --source $1 && python3 gen_symptom_images.py --source $1)
fi
echo "Finished!!"