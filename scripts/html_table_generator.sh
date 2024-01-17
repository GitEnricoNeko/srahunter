#!/bin/bash

# SRAHunter Bash Script
# Copyright (C) 2024 Bortoletto Enrico
#
# Description:
# This script processes an input file containing SRA accession numbers generating an interactive html table 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, modify, merge,and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# - Cite the pubblication or the github page into your paper

# Check for dependencies
dependencies=("figlet" "wget" "datavzrd")
for dep in "${dependencies[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        echo "Error: $dep is not installed. Please install $dep to continue."
        exit 1
    fi
done

print_usage() {
   figlet "SRAHunter"
   echo "ﾐ ᵕ̣̣ ﻌ ᵕ̣̣ ﾐ Hi guys, here the instructions !"
   
   echo "./html_table_generator.sh [output_dir]"
}

while getopts "h" o; do
  case "${o}" in
    h)   print_usage 
         exit 1;;
    ?)   print_usage
         exit 1 ;;
  esac
done

echo ' ﾐ ᵕ̣̣ ﻌ ᵕ̣̣ ﾐ '
figlet "SRAHunter"
wget https://raw.githubusercontent.com/GitEnricoNeko/SRAHunter/main/utils/SRAHunter_config.yaml
datavzrd SRAHunter_config.yaml -o "$1"
rm SRAHunter_config.yaml
