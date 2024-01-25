<p align="center">
<img src='logo/SRA-HUNTER_logo.png' width='400'>
</p>

## SRAHunter 

#### Description
SRAHunter is a set of tools designed to facilitate the downloading and processing of data and metadata from the Sequence Read Archive (SRA). This package includes two main scripts: a Python script for automatized download of fastq files from SRA (SRA_downdumper.py) and a Bash script for SRA associated metadata retrieval (SRA_metadata).

#### Installation
As part of the conda repository to install srahunter you can simply use this command 

I suggest to use mamba to speed-up the installation process 

```
mamba install enriconeko::srahunter
``` 

or as an alternative 
 
```
conda install enriconeko::srahunter
``` 

### Scripts
#### `SRA_downdumper.py`: 
Download and dump files using an accession list from SRA. This script take as an input simply an SRA accession list downloaded by the user from SRA and perform the download of the .sra file and the subsequent conversion in single or paired fastq files.

This script has been tested for all the main sequencing platforms so can be used to download data prdouced with Illumina, PACBio and Oxford Nanopore platforms.

**Usage Example:** `python SRA_downdumper.py -l <accession_list.txt>  <other options>`

 ##### Main functionality:
- Automatic removal of .sra file after sucessfull dumping the user don't need to do it manually
- Check disk space at the beginning of the download of every sample (at least 20G of disk required). If the disk is almost full the script will stop with an error message
- Remember of the already sucessfull processed data and in case of interruption the script will resume
- Writing of the failed file download in a specific file (failed_list.csv) 

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
<kbd><span class="option">--list , -l </span></kbd></td>
<td>Accession list from SRA (realtive or full file path)</td></tr>
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



#### `SRA_metadata`: 

This Bash script handles the retrieval of metadata from the NCBI SRA database, splits large input files into manageable chunks, and organizes the fetched data in a final complete table 'SRA_info.csv' and will produce an interactive table in the folder SRA_html.

##### Main functionality:
- Really fast retrival exploiting the entrez-direct functionality 
- Collection of all the metadata in a CSV table easy handable by the user to perform further analysis 
- Producing an HTML interactive table with link to SRA, chart summariseing the data, and the possibility of filtering the data 

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
<td>Accession list from SRA (realtive or full file path)</td></tr>
<tr><td class="option-group">
</tbody>
</table>
</dd>
</dl>
