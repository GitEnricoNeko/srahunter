<p align="center">
<img src='logo/SRA-HUNTER_logo.png' width='400'>
</p>

## SRAHunter 

#### Description
SRAHunter is a tool designed to facilitate the downloading and processing of data and metadata from the Sequence Read Archive ([SRA](https://www.ncbi.nlm.nih.gov/sra)) of the National Center for Biotechnology Information ([NCBI](https://www.ncbi.nlm.nih.gov/)). This package includes three modules : a module for automatized download of fastq files from SRA (srahunter download), a module for main SRA associated metadata retrieval (srahunter metadata), and a module to retrieve the full associated metadata to an accession number (srahunter fullmetadata).

#### Installation
As part of the conda repository to install srahunter you can simply use this command 

I suggest to use mamba to speed-up the installation process 

```
mamba install -c bioconda enriconeko::srahunter
``` 

or as an alternative 
 
```
conda install -c bioconda enriconeko::srahunter
``` 

Also the installation with pip is available with:



### Scripts
#### `srahunter download`: 
Using an SRA accession list downloaded by the user from SRA as input the tool perform the download of the SRA files and the subsequent conversion to single or paired FASTQ files.

This script has been tested for the main sequencing platforms so can be used to download data produced with Illumina, PACBio and ONT platforms.

 ##### Usage Example: `srahunter download -l <accession_list.txt>  <other options>`



 ##### Main functionality:
- Automatic removal of .sra files after successfull dumping, the user don't need to do it manually
- Check disk space at the beginning of every sample download (at least 20G of disk required). If the disk is almost full the script will stop with an error message
- Remember of the already successfull processed data and, in case of interruption, the script will resume
- Writing of the failed downloads in a file (failed_list.csv) 

 ##### Options:
<dl class="docutils">
<dd><table class="first last docutils option-list" frame="void" rules="none">
<col class="option" />
<col class="description" />
<tbody valign="top">
<tr><td class="option-group">
<kbd><span class="option">-h</span></kbd></td>
<td>Show help message and exit</td></tr>
<tr><td class="option-group">
<kbd><span class="option">--list , -i </span></kbd></td>
<td>Accession list from SRA (relative or full file path)</td></tr>
<tr><td class="option-group">
<kbd><span class="option">-t</span></kbd></td>
<td>Number of threads (default: 6)</td></tr>
<tr><td class="option-group">
<kbd><span class="option">--path,-sra-path,-p</span></kbd></td>
<td>Path to where to download .sra files (default: currentdirectory/tmp_srahunter</td></tr>
<tr><td class="option-group">
<kbd><span class="option">--maxsize,-ms</span></kbd></td>
<td>Max size of each sra file (default: 50G)</td></tr>
 <tr><td class="option-group">
<kbd><span class="option">--outdir,-o</span></kbd></td>
<td>Path to where to download .fastq files (default: currentdirectory)</td></tr>
</tbody>
</table>
</dd>
</dl>

Attention!! For the moment only accession Run numbers are supported (e.g. SRR8487013) and must be included in an accession list 



#### `srahunter metadata`: 

This module handles the retrieval of metadata from the NCBI SRA database, splits large input files into manageable chunks, and organizes the fetched data in a final table 'SRA_info.csv'. The module will alsom produce an interactive table in the folder SRA_html. In this case the module will download the most used metadata associated to a Run accession number.

 ##### Usage Example: `srahunter metadata -i <accession_list.txt>`


##### Main functionalities:
- Fast data retrieval with Entrez-direct 
- Metadata collection in a clean CSV format 
- HTML interactive table with links to SRA, a chart summarising the data, and the possibility to apply filters 

##### Options:
<dl class="docutils">
<dd><table class="first last docutils option-list" frame="void" rules="none">
<col class="option" />
<col class="description" />
<tbody valign="top">
<tr><td class="option-group">
<kbd><span class="option">-h</span></kbd></td>
<td>Show help message and exit</td></tr>
<tr><td class="option-group">
<kbd><span class="option">-i</span></kbd></td>
<td>Accession list from SRA (relative or full file path)</td></tr>
</tbody>
</table>
</dd>
</dl>



#### `srahunter fullmetadata`: 

This module handles the retrieval of metadata from the NCBI SRA database, splits large input files into manageable chunks, and organizes the fetched data in a final full table 'Full_SRA_info.csv'. In this case the module will download all the metadata associated to a Run accession number.

 ##### Usage Example: `srahunter fullmetadata -i <accession_list.txt>`


##### Main functionalities:
- Fast data retrieval with Entrez-direct 
- Metadata collection in a clean CSV format 

##### Options:
<dl class="docutils">
<dd><table class="first last docutils option-list" frame="void" rules="none">
<col class="option" />
<col class="description" />
<tbody valign="top">
<tr><td class="option-group">
<kbd><span class="option">-h</span></kbd></td>
<td>Show help message and exit</td></tr>
<tr><td class="option-group">
<kbd><span class="option">-i</span></kbd></td>
<td>Accession list from SRA (relative or full file path)</td></tr>
</tbody>
</table>
</dd>
</dl>
#### Error Handling and Troubleshooting
If you encounter any issues or errors while using SRAHunter, please check the following common problems:
- Ensure that your Conda or Mamba environment is correctly set up.
- Verify that the format of your SRA accession list is correct.
- Check available disk space if you encounter download issues.

For more help, please open an issue on the [GitHub repository](https://github.com/GitEnricoNeko/SRAHunter/issues).

#### Contributing
Contributions to SRAHunter are welcome! Please read our contributing guidelines on the [GitHub repository](https://github.com/GitEnricoNeko/SRAHunter) for instructions on how to contribute.

#### License
SRAHunter is released under the [MIT License](https://opensource.org/licenses/MIT).

#### Acknowledgments
Special thanks to ....

