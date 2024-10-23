import os
import subprocess
import argparse
import pyfiglet
import pandas as pd
from tqdm import tqdm
import sys
from tempfile import NamedTemporaryFile
from io import StringIO
import xml.etree.ElementTree as ET

# Version
__version__ = '0.0.4'

def print_ascii_art():
    text = "srahunter"
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
        sys.exit(1)

def extract_sample_attributes(sample_info):
    attributes = {}
    for attr in sample_info.findall('.//SAMPLE_ATTRIBUTE'):
        tag = attr.find('TAG').text
        value = attr.find('VALUE').text
        attributes[tag] = value
    return attributes

def extract_detailed_run_info(run):
    run_info = { 'Run Accession': run.attrib.get('accession', ''),
                 'Total Spots': run.find('.//Statistics').attrib.get('total_spots', ''),
                 'Total Bases': run.find('.//Statistics').attrib.get('total_bases', ''),
                 'Size': run.attrib.get('size', ''),
                 'Published Date': run.attrib.get('published', '') }
    sra_files = run.findall('.//SRAFile')
    run_info['SRA File Count'] = len(sra_files)
    cloud_files = run.findall('.//CloudFile')
    cloud_file_types = ", ".join(set(cf.get('filetype', '') for cf in cloud_files))
    run_info['Cloud File Types'] = cloud_file_types
    statistics = run.find('.//Statistics')
    if statistics is not None:
        run_info['Statistics Nreads'] = statistics.get('nreads', '')
        run_info['Statistics Nspots'] = statistics.get('nspots', '')
    bases = run.find('.//Bases')
    if bases is not None:
        run_info['Base Count'] = bases.get('count', '')
    return run_info

def remove_commas_from_xml(xml_path):
    with open(xml_path, 'r', encoding='utf-8') as file:
        xml_content = file.read()
    modified_xml_content = xml_content.replace(',', '')
    return modified_xml_content

def extract_info(package):
    info = {}
    exp = package.find('.//EXPERIMENT')
    if exp is not None:
        info.update({
            'Experiment Accession': exp.get('accession', ''),
            'Experiment Alias': exp.get('alias', ''),
            'Experiment Title': exp.find('TITLE').text if exp.find('TITLE') is not None else '',
            'Study Accession': exp.find('.//STUDY_REF').get('accession') if exp.find('.//STUDY_REF') is not None else '',
            'Study Primary ID': exp.find('.//PRIMARY_ID').text if exp.find('.//PRIMARY_ID') is not None else '',
            'Study External ID': exp.find('.//EXTERNAL_ID').text if exp.find('.//EXTERNAL_ID') is not None else '',
            'Design Description': exp.find('.//DESIGN_DESCRIPTION').text if exp.find('.//DESIGN_DESCRIPTION') is not None else '',
            'Sample Descriptor Accession': exp.find('.//SAMPLE_DESCRIPTOR').get('accession') if exp.find('.//SAMPLE_DESCRIPTOR') is not None else '',
            'Library Name': exp.find('.//LIBRARY_NAME').text if exp.find('.//LIBRARY_NAME') is not None else '',
            'Library Strategy': exp.find('.//LIBRARY_STRATEGY').text if exp.find('.//LIBRARY_STRATEGY') is not None else '',
            'Library Source': exp.find('.//LIBRARY_SOURCE').text if exp.find('.//LIBRARY_SOURCE') is not None else '',
            'Library Selection': exp.find('.//LIBRARY_SELECTION').text if exp.find('.//LIBRARY_SELECTION') is not None else '',
            'Library Layout': 'PAIRED' if exp.find('.//LIBRARY_LAYOUT/PAIRED') is not None else 'SINGLE',
            'Instrument Model': exp.find('.//INSTRUMENT_MODEL').text if exp.find('.//INSTRUMENT_MODEL') is not None else ''
        })

    sub = package.find('.//SUBMISSION')
    if sub is not None:
        info.update({
            'Submission Accession': sub.get('accession', ''),
            'Submission Alias': sub.get('alias', ''),
            'Submission Lab Name': sub.get('lab_name', ''),
            'Submission Center Name': sub.get('center_name', ''),
            'Submission Primary ID': sub.find('.//PRIMARY_ID').text if sub.find('.//PRIMARY_ID') is not None else '',
            'Submitter ID': sub.find('.//SUBMITTER_ID').text if sub.find('.//SUBMITTER_ID') is not None else ''
        })

    study_info = package.find('.//STUDY')
    if study_info is not None:
        info.update({
            'Study Center Name': study_info.get('center_name', ''),
            'Study Alias': study_info.get('alias', ''),
            'Study Title': study_info.find('.//STUDY_TITLE').text if study_info.find('.//STUDY_TITLE') is not None else '',
            'Study Abstract': study_info.find('.//STUDY_ABSTRACT').text if study_info.find('.//STUDY_ABSTRACT') is not None else ''
        })

    sample_info = package.find('.//SAMPLE')
    if sample_info is not None:
        sample_attributes = extract_sample_attributes(sample_info)
        info.update({
            'Sample Alias': sample_info.get('alias', ''),
            'Sample Accession': sample_info.get('accession', ''),
            'Scientific Name': sample_info.find('.//SCIENTIFIC_NAME').text if sample_info.find('.//SCIENTIFIC_NAME') is not None else '',
            **sample_attributes
        })
    pools = package.findall('.//Pool/Member')
    info['Pool Member Count'] = len(pools)
    run_set = package.find('.//RUN_SET')
    if run_set is not None:
        first_run = run_set.find('.//RUN')
        if first_run is not None:
            run_info = extract_detailed_run_info(first_run)
            info.update(run_info)
    return info

def process_files(file_list):
    new_root = ET.Element("SRA_Results")
    for line in tqdm(file_list, desc='Processing', unit='file', leave=False):
        with NamedTemporaryFile(delete=False) as temp_file:
            subprocess.run(["efetch", "-input", line, "-db", "sra", "-format", "xml"], stdout=temp_file)
            temp_file_path = temp_file.name
        tree = ET.parse(temp_file_path)
        root = tree.getroot()
        for child in root:
            new_root.append(child)
        os.remove(temp_file_path)
        os.remove(line)
    new_tree = ET.ElementTree(new_root)
    new_tree.write("SRA_info.xml")

def convert_xml_to_csv(xml_path, csv_path):
    modified_xml_content = remove_commas_from_xml(xml_path)
    tree = ET.parse(StringIO(modified_xml_content))
    root = tree.getroot()
    data = [extract_info(pkg) for pkg in root.findall('.//EXPERIMENT_PACKAGE')]
    df = pd.DataFrame(data)
    df.to_csv(csv_path, index=False)
    print(f"Data saved to {csv_path}.")

def main(args):
    check_dependencies()

    input_file = args.list
    print('Preparing files for processing...')
    os.makedirs("tmp_neko", exist_ok=True)
    os.makedirs("output_srahunter", exist_ok=True)

    # Read the input file and filter out lines that contain 'acc'
    with open(input_file, "r") as f:
        lines = [line for line in f if 'acc' not in line]
        for i, chunk in enumerate(range(0, len(lines), 100)):
            with open(os.path.join("tmp_neko", f"part_{i}.txt"), "w") as chunk_file:
                chunk_file.writelines(lines[chunk:chunk+100])

    file_list = [os.path.join(dirpath, filename) for dirpath, _, filenames in os.walk("tmp_neko") for filename in filenames]

    process_files(file_list)
    convert_xml_to_csv("SRA_info.xml", "Full_SRA_info.csv")

    input_df = pd.read_csv(args.list, header=None)
    input_list = input_df.iloc[:, 0]
    
    csv_df = pd.read_csv("Full_SRA_info.csv")
    column_name = "Run Accession"
    column_data = csv_df[column_name]
    
    # Find missing accessions (those in input_list but not in column_data)
    missing_accessions = input_list[~input_list.isin(column_data)]
    missing_accessions_filtered = missing_accessions[~missing_accessions.str.contains('acc', case=False)]
    missing_accessions = missing_accessions_filtered
    if not missing_accessions.empty:
        missing_accessions.to_csv("output_srahunter/failed_metadata.csv", index=False, header=False)
        failed = missing_accessions.shape[0]
        print(f"Impossible to retrieve metadata information for {failed} samples, check failed_metadata.csv for more information")
    else:
        print("All metadata successfully retrieved and saved in output_srahunter folder CSV: Full_SRA_info.csv")
        print("Thank you for choosing SRAhunter, please remember to cite our publication or the GitHub page")

    os.rename("Full_SRA_info.csv", "output_srahunter/Full_SRA_info.csv")
    os.remove("SRA_info.xml")
    os.rmdir("tmp_neko")

if __name__ == "__main__":
    parser = ArgumentParserWithErrorHandling(description='srahunter: Download and dump files using an accession list from SRA')
    parser.add_argument('--list', '-i', help='Accession list from SRA (file path)', required=True)
    parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}', help="Show program's version number and exit")        
    args = parser.parse_args()
    main(args)
