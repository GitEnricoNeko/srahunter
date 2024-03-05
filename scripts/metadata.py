import os
import subprocess
import argparse
import pyfiglet
from tqdm import tqdm
import sys

def print_ascii_art():
    text = "SRAHunter"
    ascii_art = pyfiglet.figlet_format(text)
    print(ascii_art)

class ArgumentParserWithErrorHandling(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write(f'error: {message}\n')
        self.print_help()
        sys.exit(2)

def check_dependencies():
    dependencies = ["efetch", "realpath"]
    missing_deps = [dep for dep in dependencies if subprocess.run(["which", dep], capture_output=True, text=True).returncode != 0]
    if missing_deps:
        print(f"Error: {' and '.join(missing_deps)} {'are' if len(missing_deps) > 1 else 'is'} not installed. Please install {'them' if len(missing_deps) > 1 else 'it'} to continue.")
        sys.exit(1)  # Use sys.exit for consistency

print_ascii_art()

def main(args):
    check_dependencies()

    input_file = args.list  # Adjusted to use the correct argument name
    print('Splitting your file into smaller files...')
    os.makedirs("tmp_neko", exist_ok=True)
    os.makedirs("output_srahunter", exist_ok=True)

    with open(input_file, "r") as f:
        lines = f.readlines()
        for i, chunk in enumerate(range(0, len(lines), 100)):
            with open(os.path.join("tmp_neko", f"part_{i}.txt"), "w") as chunk_file:
                chunk_file.writelines(lines[chunk:chunk+100])

    file_list = []
    for dirpath, _, filenames in os.walk("tmp_neko"):
        for filename in filenames:
            file_list.append(os.path.realpath(os.path.join(dirpath, filename)))

    with open("SRA_info.csv", "w") as f:
        headers = 'Run,ReleaseDate,LoadDate,spots,bases,spots_with_mates,avgLength,size_MB,AssemblyName,download_path,Experiment,LibraryName,LibraryStrategy,LibrarySelection,LibrarySource,LibraryLayout,InsertSize,InsertDev,Platform,Model,SRAStudy,BioProject,Study_Pubmed_id,ProjectID,Sample,BioSample,SampleType,TaxID,ScientificName,SampleName,g1k_pop_code,source,g1k_analysis_group,Subject_ID,Sex,Disease,Tumor,Affection_Status,Analyte_Type,Histological_Type,Body_Site,CenterName,Submission,dbgap_study_accession,Consent,RunHash,ReadHash\n'
        f.write(headers)

    with tqdm(total=len(file_list), desc='Processing', unit='file', leave=False, position=0) as pbar:        
        for line in file_list:
            subprocess.run(["efetch", "-input", line, "-db", "sra", "-format", "runinfo"], stdout=open("SRA_info_prov.txt", "w"))
            with open("SRA_info_prov.txt", "r") as prov_file:
                next(prov_file)  # Skip header
                with open("SRA_info.csv", "a") as csv_file:
                    for prov_line in prov_file:
                        csv_file.write(prov_line)
            os.remove("SRA_info_prov.txt")
            pbar.update(1)
            os.remove(line)

    subprocess.run(["wget", "https://raw.githubusercontent.com/GitEnricoNeko/SRAHunter/main/utils/SRAHunter_config.yaml", "-q"])
    subprocess.run(["datavzrd", "SRAHunter_config.yaml", "-o", "output_srahunter/SRA_html", "--overwrite-output"])
    os.remove("SRAHunter_config.yaml")
    os.rmdir("tmp_neko")

    error = subprocess.getoutput(f"cat SRA_info.csv {input_file} | cut -f1 -d, | sort | uniq -c | grep -E \"^ *1 \" | grep -v \"Run\" | sed 's/^ *1 //'")
    os.rename("SRA_info.csv", "output_srahunter/SRA_info.csv")
    if error:
        with open("output_srahunter/failed_metadata.csv", "w") as f:
            f.write(error)
        failed = sum(1 for _ in open("output_srahunter/failed_metadata.csv"))
        print(f"Impossible to retrieve metadata information for {failed} samples, check failed_metadata.csv for more information")
    else:
        print("All metadata successfully retrieved and saved in output_srahunter folder CSV: SRA_info.csv and interactive html: SRA_html folder (double-click on index.html file)")
    print("Thank you for choosing SRAhunter, please remember to cite our publication or the GitHub page")

if __name__ == "__main__":
    parser = ArgumentParserWithErrorHandling(
        description='SRAHunter: Download and dump files using an accession list from SRA')
    parser.add_argument('--list', '-i', help='Accession list from SRA (file path)', required=True)
    args = parser.parse_args()
    main(args)
