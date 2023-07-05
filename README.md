# sequence_collapsing
Python scripts to collapse sequences into unique sequences

## Installation

Clone this repository in your designated directory
```
git clone https://github.com/MullinsLab/sequence_collapsing.git
```
  - it will create a directory called "sequence_collapsing" in your designated directory (i.e. WhereSequenceCollapsingInstalled)

## Usage
### Collapsing sequences
In a working directory that contains sequence fasta file (filename.fasta), run following command to collapse sequences in the fasta file into unique sequences
````
python WhereSequenceCollapsingInstalled/collapse_sequences.py filename.fasta
````
  - it will output two files. One is the collapsed unique sequence fasta file (filename_collapsed.fasta), the other is the name file that is tab delimited text file listing the unique sequence names and corresponding original sequence names (filename_collapsed_name.txt)

Or, run following command to collapse sequences in the fasta file into unique sequences based on groups/timepoints
````
python WhereSequenceCollapsingInstalled/collapse_sequences_by_groups.py filename.fasta
````
  - in order to collapse sequences based on groups/timepoints, the sequence names have to follow the pattern of *"projectID_sampleID_group_region_somethingElse"*
  - it will output two files. One is the collapsed unique sequence fasta file (filename_collapsed_by_grp.fasta), the other is the name file that is tab delimited text file listing the unique sequence names and corresponding original sequence names (filename_collapsed_by_grp_name.txt)
### Uncollapsing sequences
In a working directory that contains collapsed unique sequence fasta file and the name file, run following command to uncollapse unique sequences in the collapsed sequence fasta file into the original uncollapsed sequences
````
python WhereSequenceCollapsingInstalled/uncollapse_sequences.py filename.fasta namefile
````
  - it will output the uncollapsed sequence fasta file (filename_uncollapsed.fasta)
