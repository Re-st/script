#!/bin/bash

for folder in *; do
  if [ -d "$folder" ]; then
    for file in "$folder"/*; do
      if [ -f "$file" ]; then
        mv "$file" "./$folder+${file##*/}"
      fi
    done
    rmdir $folder
  fi
done
