import os
import argparse
from .download import main as download_main
from .metadata import main as metadata_main
from .fullmetadata import main as fullmetadata_main

# Define version
__version__ = '0.0.4'

def main():
    parser = argparse.ArgumentParser(description="srahunter Tool")
    parser.add_argument('--version', action='version', version=f'srahunter version {__version__}')
    
    # Create subparsers for each subcommand
    subparsers = parser.add_subparsers(dest='command')

    # Download command
    parser_download = subparsers.add_parser('download', help='Download data')
    parser_download.add_argument('--list', '-i', required=True, help='Accession list from SRA (file path)')
    parser_download.add_argument('-t', type=int, default=6, help='Number of threads (default: 6)')
    parser_download.add_argument('--path', '-p', default=os.path.join(os.getcwd(), 'tmp_srahunter'), help='Path to where to download .sra files (default: current directory/tmp_srahunter)')
    parser_download.add_argument('--maxsize', '-ms', default="50G", help='Max size of each sra file (default: 50G)')
    parser_download.add_argument('--outdir', '-o', default=os.getcwd(), help='Path to where to download .fastq files (default: current directory)')

    # Metadata command
    parser_metadata = subparsers.add_parser('metadata', help='Fetch metadata')
    parser_metadata.add_argument('--list', '-i', required=True, help='Accession list from SRA (file path)')
    parser_metadata.add_argument('--no-html', action='store_true', help='Disable HTML table generation')

    # Fullmetadata command
    parser_fullmetadata = subparsers.add_parser('fullmetadata', help='Fetch full metadata')
    parser_fullmetadata.add_argument('--list', '-i', required=True, help='Accession list from SRA (file path)')

    args = parser.parse_args()

    # Determine which command is called and invoke the appropriate function
    if args.command == 'download':
        download_main(args)
    elif args.command == 'metadata':
        metadata_main(args)
    elif args.command == 'fullmetadata':
        fullmetadata_main(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
