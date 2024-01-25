#!/usr/bin/env python3
import subprocess
import pandas as pd
import argparse
import sys
import os
import psutil
import pyfiglet

# Display SRAHunter in ASCII art format using pyfiglet
print(pyfiglet.figlet_format("SRAHunter"))


class ArgumentParserWithErrorHandling(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)

default_dir = os.path.join(os.getcwd(), 'tmp_srahunter')
# Argument specification
parser = ArgumentParserWithErrorHandling(
    description='SRAHunter: Download and dump files using an accession list from SRA')
parser.add_argument('--list','-l', help='Accession list from SRA (file path)', required=True)
parser.add_argument('-t', type=int, default=6, help='Number of threads (default: 6)')
parser.add_argument('--path', '-sra-path','-p', default=default_dir, help='Path to where to download .sra files (default: currentdirectory/tmp_srahunter')
parser.add_argument('--maxsize','-ms',default="50G", help='Max size of each sra file (default: 50G)')
parser.add_argument('--outdir', '-o', default=os.getcwd(), help='Path to where to download .fastq files (default: currentdirectory')

args = parser.parse_args()

# Output directory to be created
dir_name = "tmp_srahunter"

# Check if directory already exists
if not os.path.exists(dir_name):
    # Create a new directory
    os.mkdir(dir_name)
    print(f"Directory '{dir_name}' created.")
else:
    print(f"Directory '{dir_name}' already exists.")

# Validate the accession list file
if not os.path.isfile(args.list):
    print(f"Error: The specified file '{args.list}' does not exist.")
    sys.exit(1)

# Validate the number of threads
if args.t < 1:
    print("Error: Number of threads must be at least 1.")
    sys.exit(1)


# Reading SRA numbers
dataset = args.list
sra_numbers = pd.read_table(dataset, header=None, names=["sra_id"])

# Handle skip_list 
# Read remind_list to skip already processed samples
remind_list_path = "remind_list.csv"
if os.path.isfile(remind_list_path):
    remind_list = pd.read_csv(remind_list_path, header=None, names=["sra_id"])
else:
    remind_list = pd.DataFrame(columns=["sra_id"])

for index, row in sra_numbers.iterrows():
    sra_id = row['sra_id']
    if sra_id in remind_list['sra_id'].values:
        continue  # Skip if already processed
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

    print("There is enough free space on the device. Continuing with the script.")
    print(f"Currently downloading: {sra_id}")
    prefetch = f"prefetch -p -X {args.maxsize} {sra_id} --output-file {args.path}/{sra_id}.sra"
    print(f"The command used was: {prefetch}")
    subprocess.call(prefetch, shell=True)

    print(f"Generating fastq for: {sra_id}")
   # Running fasterq-dump command
    fasterq_dump_cmd = f"fasterq-dump --skip-technical -p -e {args.t} {args.path}/{sra_id}.sra --outdir {args.outdir}"
    print(f"The command used was: {fasterq_dump_cmd}")
    result = subprocess.call(fasterq_dump_cmd, shell=True)

    # Check if fasterq-dump was successful
    if result == 0:
        # fasterq-dump was successful, add to remind list
        with open("remind_list.csv", "a") as f:
            f.write(sra_id + "\n")

        # Proceed with other commands
        rm_cmd = f"rm {args.path}/{sra_id}.sra"
        subprocess.call(rm_cmd, shell=True)
    else:
        print(f"Error in processing {sra_id}, skipping...")
        with open(f"{args.path}/failed_list.csv", "a") as f:
         f.write(sra_id + "\n")


#Removing temporary files

os.remove("remind_list.csv") 
dir_path =args.path

# Attempt to remove the directory and printing acknowledgments 
try:
    os.rmdir(dir_path)
    print(pyfiglet.figlet_format("SRAHunter"))
    print(f"All samples sucessful processed ")
    print(f"Thank you for choosing SRAhunter please remember to cite our pubblication: or the github page ")
except OSError as error:
    print(pyfiglet.figlet_format("SRAHunter"))
    print(f"Some samples were not properly downloaded check {args.path}/failed_list.csv")
    print(f"Thank you for choosing SRAhunter please remember to cite our pubblication: or the github page ")