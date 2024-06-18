#!/bin/bash

MASTER_FILE_SUFFIX="_collection.csv"

# Loop over each directory
for dir in data/*; do

    # Check if the directory contains files
    if [ -d $dir ]; then

        echo '"Value","Count","Amount","Filename"' > "${dir}${MASTER_FILE_SUFFIX}"

        # Loop over each file in the directory
        for file in $dir/*.csv; do
            # Check if it's a regular file
            if [ -f "$file" ] ; then

                # Drop the header and add a column with the filename to each row and append to the master file
                awk -v filename="$file" '{if (NR!=1) {print $0 "," filename}}' "$file" >> "${dir}${MASTER_FILE_SUFFIX}"

            fi
        done
    fi
done
