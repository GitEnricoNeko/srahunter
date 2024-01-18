#!/bin/bash

# SRAHunter Bash Script
# Copyright (C) 2024 Bortoletto Enrico
#
# Description:
# This script processes an input file containing SRA accession numbers. It splits the file into smaller parts, 
# retrieves metadata for each accession number from the NCBI SRA database using efetch, and compiles this metadata 
# into a single file. It's designed to handle large sets of accession numbers by breaking them into manageable chunks.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, modify, merge,and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# - Cite the pubblication or the github page into your paper

# Check for dependencies
dependencies=( "efetch" "realpath")
for dep in "${dependencies[@]}"; do
    if ! command -v "$dep" &> /dev/null; then
        echo "Error: $dep is not installed. Please install $dep to continue."
        exit 1
    fi
done

print_usage() {
   python pyfiglet_wrapper.py "SRAHunter"
   echo "ﾐ ᵕ̣̣ ﻌ ᵕ̣̣ ﾐ Hi guys, here the instructions !"
   echo "       -h print tool help"
   echo "       -i input file (mandatory)"
}

while getopts "i:h" o; do
  case "${o}" in
    i) i="$OPTARG" ;;
    h) print_usage 
       exit 1 ;;
    ?) print_usage
       exit 1 ;;
  esac
done

if [ -z "$i" ]; then
    echo "Error: Input file not specified."
    print_usage
    exit 1
fi

echo ' ﾐ ᵕ̣̣ ﻌ ᵕ̣̣ ﾐ '
python pyfiglet_wrapper.py "SRAHunter"
echo -ne 'ﾐ ᵕ̣̣ ﻌ ᵕ̣̣ ﾐ splitting your file in smaller files\033[0K\r'
mkdir -p tmp_neko
split -l 100 "$i" tmp_neko/part_
a=$(wc -l < "$i")
find . -type f -name "part_*" -print0 | xargs -0 realpath > tmp_neko/file_list

# Header for the final output file
echo 'Run,ReleaseDate,LoadDate,spots,bases,spots_with_mates,avgLength,size_MB,AssemblyName,download_path,Experiment,LibraryName,LibraryStrategy,LibrarySelection,LibrarySource,LibraryLayout,InsertSize,InsertDev,Platform,Model,SRAStudy,BioProject,Study_Pubmed_id,ProjectID,Sample,BioSample,SampleType,TaxID,ScientificName,SampleName,g1k_pop_code,source,g1k_analysis_group,Subject_ID,Sex,Disease,Tumor,Affection_Status,Analyte_Type,Histological_Type,Body_Site,CenterName,Submission,dbgap_study_accession,Consent,RunHash,ReadHash' > SRA_info.txt

#Obtaining metadata from SRA
while read -r line; do 
    efetch -input "$line" -db sra -format runinfo | tail -n +2 >> SRA_info_prov.txt
    awk 'BEGIN{FS=OFS=","}  FNR==NR{arr[$1];next} (($1) in arr)' "$line" SRA_info_prov.txt >> SRA_info.txt
    b=$(wc -l < SRA_info.txt)
    echo -ne 'ﾐ ᵕ̣̣ ﻌ ᵕ̣̣ ﾐ retrieving metadata from NCBI sra '$b'-'$a'\033[0K\r'
    rm "$line" SRA_info_prov.txt
done < tmp_neko/file_list

rm -rf tmp_neko

