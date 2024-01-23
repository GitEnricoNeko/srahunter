![SRA-HUNTER logo_EB_RF_22jan24](https://github.com/GitEnricoNeko/SRAHunter/assets/75318813/1fed43fc-07a7-443d-ada0-0464b5cf95e3 | width=100)

## SRAHunter 

#### Description
SRAHunter is a set of tools designed to facilitate the downloading and processing of data from the Sequence Read Archive (SRA). This package includes two main scripts: a Python script for automatized download of fastq files form SRA (SRA_downdumper.py) and a Bash script for SRA associated metadata retrieval (SRA_metadata).

### Scripts
#### `SRA_downdumper.py`: 
Download and dump files using an accession list from SRA. This script take as an input simply an SRA accession list downloaded by the user from SRA and perform the download of the .sra file and the subsequent conversion in single or paired fastq files.
 ##### Main functionality:
- Automatic removal of .sra file after sucessfull dumping
- Check disk space at the beginning of the download of every sample (at least 20G of disk required). If the disk is almost full the script will stop with an error message 

 ##### Options:
<dl class="docutils">
<dd><table class="first last docutils option-list" frame="void" rules="none">
<col class="option" />
<col class="description" />
<tbody valign="top">
<tr><td class="option-group">
<kbd><span class="option">-h</span></kbd></td>
<td>show help message and exit</td></tr>
<tr><td class="option-group">
<kbd><span class="option">--list</span></kbd></td>
<td>Accession list from SRA (realtive or full file path)</td></tr>
<tr><td class="option-group">
<kbd><span class="option">-t</span></kbd></td>
<td>Number of threads (default: 6)</td></tr>
<tr><td class="option-group">
<kbd><span class="option">--path</span></kbd></td>
<td>Path to SRA folder (default: ~/ncbi/public/sra/)</td></tr>
<tr><td class="option-group">
<kbd><span class="option">--maxsize</span></kbd></td>
<td>Max size of each fastq file (default: 50G)</td></tr>
</tbody>
</table>
</dd>
</dl>

Attention!! For the moment only accession Run numbers are supported (e.g. SRR8487013) and must be included in an accession list 


- `SRA_full_metadata.sh`: This Bash script handles the retrieval of metadata from the NCBI SRA database, splits large input files into manageable chunks, and organizes the fetched data.


