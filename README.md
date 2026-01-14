# Sequence Collapsing Tool

A Python tool for collapsing identical sequences in FASTA files into unique sequences and restoring them back to their original form.

## Features

- Collapses identical DNA/RNA sequences into unique representatives
- Supports field-based grouping for sequence names
- Deterministic output (sequences with the same abundance are alphabetically sorted)
- Tracks abundance and original sequence names
- Reversible process through uncollapsing

## Installation

Clone this repository:
```bash
git clone https://github.com/MullinsLab/sequence_collapsing.git
cd sequence_collapsing
```

No additional dependencies required - uses Python standard library only.

## Usage

### Collapsing Sequences

#### Basic Usage - Collapse All Sequences

Collapse all identical sequences in a FASTA file:

```bash
python collapse_sequences.py input.fasta
```

**Output files:**
- `input_collapsed.fasta` - Collapsed unique sequences
- `input_collapsed_name.txt` - Mapping file (tab-delimited)

**Collapsed sequence naming format:** `{id}_{uniqueNumber}_{abundance}`

Example: `sample1_1_5` means the first unique sequence with 5 copies

#### Advanced Usage - Collapse by Name Fields

Collapse sequences grouped by specific fields in the sequence name:

```bash
python collapse_sequences.py input.fasta -i 1,2,3
```

This groups sequences by fields 1, 2, and 3 of underscore-separated sequence names.

**Example:**
If your sequence names follow the pattern: `projectID_sampleID_timepoint_region_other`
- `-i 1` - Collapse by project only
- `-i 1,2` - Collapse by project and sample
- `-i 1,2,3` - Collapse by project, sample, and timepoint

**Output files:**
- `input_collapsed_by_field123.fasta`
- `input_collapsed_by_field123_name.txt`

### Uncollapsing Sequences

Restore collapsed sequences back to their original form:

```bash
python uncollapse_sequences.py collapsed.fasta collapsed_name.txt
```

**Output:**
- `collapsed_uncollapsed.fasta` - Restored original sequences

## File Formats

### Input FASTA File
Standard FASTA format with sequence names starting with `>`:
```
>sequence1_sample_timepoint_region
ATCGATCGATCG
>sequence2_sample_timepoint_region
ATCGATCGATCG
>sequence3_sample_timepoint_region
GCTAGCTAGCTA
```

### Output Collapsed FASTA
Unique sequences with abundance information:
```
>sample_timepoint_region_1_2
ATCGATCGATCG
>sample_timepoint_region_2_1
GCTAGCTAGCTA
```

### Output Name Mapping File
Tab-delimited file mapping collapsed names to original names:
```
sample_timepoint_region_1_2    sequence1_sample_timepoint_region,sequence2_sample_timepoint_region
sample_timepoint_region_2_1    sequence3_sample_timepoint_region
```

## Key Features

### Deterministic Output
The script ensures reproducible results by sorting sequences with the same abundance alphabetically. Running the same input multiple times will always produce identical output.

### Abundance-Based Ordering
Within each group, sequences are ordered by abundance (most common first), with ties broken alphabetically.

### Flexible Grouping
The field index option allows flexible grouping strategies based on your sequence naming convention, making it suitable for analyzing sequences across different samples, timepoints, or experimental conditions.

## Requirements

- Python 3.x
- Input FASTA files must have `.fasta` extension

## Contact

For any questions, bugs and suggestions, please send email to cohnlabsupport@fredhutch.org and include a few sentences describing, briefly, the nature of your questions and include contact information.