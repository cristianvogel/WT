#!/bin/bash

# Check if an argument is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <name>"
  exit 1
fi

name="$1"
python3 wt-tool.py -a create -d incoming/RN -f "$name"
mv "$name" "/Users/cristianvogel/Library/CloudStorage/GoogleDrive-cristian.vogel55@gmail.com/My Drive/BW5.0 Sound Design/WT by NEL"