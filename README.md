# SRAHunter 

## Description
SRAHunter is a set of tools designed to facilitate the downloading and processing of data from the Sequence Read Archive (SRA). This package includes two main scripts: a Python script for automatized download of fastq files form SRA (SRA_downdumper.py) and a Bash script for SRA associated metadata retrieval (SRA_metadata).

## Scripts
### `SRA_downdumper.py`: 
Download and dump files using an accession list from SRA. This script take as an input simply an SRA accession list downloaded by the user from SRA and perform the download of the .sra file and the subsequent conversion in single or paired fastq files.
 #### Main functionality:
- Automatic removal of .sra file after sucessfull dumping
- 

 #### options:
  -h, --help         show help message and exit
  --list LIST        Accession list from SRA (file path)
  -t T               Number of threads (default: 6)
  --path PATH        Path to SRA folder (default: ~/ncbi/public/sra/)
  --maxsize MAXSIZE  Max size of each fastq file (default: 50G)

Attention!! For the moment only accession Run numbers are supported (e.g. SRR8487013) and must be included in an accession list 


- `SRA_full_metadata.sh`: This Bash script handles the retrieval of metadata from the NCBI SRA database, splits large input files into manageable chunks, and organizes the fetched data.


![SRA-HUNTER logo_EB_RF_22jan24](https://github.com/GitEnricoNeko/SRAHunter/assets/75318813/1fed43fc-07a7-443d-ada0-0464b5cf95e3)
