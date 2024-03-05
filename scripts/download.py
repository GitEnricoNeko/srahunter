#!/usr/bin/env python3
import subprocess
import pandas as pd
import argparse
import sys
import os
import psutil
import pyfiglet
import requests

def print_ascii_art():
    """Prints ASCII art for SRAHunter."""
    print(pyfiglet.figlet_format("SRAHunter"))

def main(args):
    """Handles the main downloading logic."""
    print(f"Downloading with list: {args.list}")
    print(f"Number of t: {args.t}")
    print(f"Download path: {args.path}")
    print(f"Max size: {args.maxsize}")
    print(f"Output directory: {args.outdir}")
    
    # Validate the accession list file
    if not os.path.isfile(args.list):
        print(f"Error: The specified file '{args.list}' does not exist.")
        sys.exit(1)
    
    # Validate the number of t
    if args.t < 1:
        print("Error: Number of t must be at least 1.")
        sys.exit(1)
    
    # Reading SRA numbers
    sra_numbers = pd.read_table(args.list, header=None, names=["sra_id"])
    
    # Define the minimum required free space in gigabytes
    MINIMUM_SPACE_GB = 20
    # Get the available disk space on the root ("/") partition in bytes
    available_space_bytes = psutil.disk_usage('/').free
    # Convert available space to gigabytes
    available_space_gb = available_space_bytes / (1024 ** 3)
    # Check if available space is less than the minimum required
    if available_space_gb < MINIMUM_SPACE_GB:
        print("Less than 20 Gigabytes of space on device. Dangerous to continue. Script will be stopped.")
        sys.exit(1)
    
    for sra_id in sra_numbers["sra_id"]:
        print(f"Currently downloading: {sra_id}")
        prefetch_cmd = f"prefetch -p -X {args.maxsize} {sra_id} --output-file {args.path}/{sra_id}.sra"
        print(f"The command used was: {prefetch_cmd}")
        subprocess.call(prefetch_cmd, shell=True)
        
        print(f"Generating fastq for: {sra_id}")
        fasterq_dump_cmd = f"fasterq-dump --skip-technical -p -e {args.t} {args.path}/{sra_id}.sra --outdir {args.outdir}"
        print(f"The command used was: {fasterq_dump_cmd}")
        result = subprocess.call(fasterq_dump_cmd, shell=True)
        
        # Check if fasterq-dump was successful
        if result == 0:
            print(f"Processing {sra_id} completed successfully.")
        else:
            print(f"Error in processing {sra_id}, skipping...")
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SRAHunter: Download and dump files using an accession list from SRA')
    parser.add_argument('--list', '-i', required=True, help='Accession list from SRA (file path)')
    parser.add_argument( '-t', type=int, default=6, help='Number of t (default: 6)')
    parser.add_argument('--download-path', '-p', default=default_dir, help='Path to download .sra files (default: current directory/tmp_srahunter)')
    parser.add_argument('--max-size', '-ms', default="50G", help='Max size of each sra file (default: 50G)')
    parser.add_argument('--output-dir', '-o', default=os.getcwd(), help='Path to output .fastq files (default: current directory)')
    args = parser.parse_args()
    main(args)