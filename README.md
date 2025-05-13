# Variation Project

This project is designed to analyze genetic variations by processing alignments, handling indels, and performing calculations with bootstrapping. 

The script takes input IPD-IMGT/HLA alignments, processes them, and generates JSON output files containing the results.

## Features

- Processes genetic alignments for specific genes and levels (nucleotide, protein, or genomic).
- Handles indels in alignments using custom processing functions.
- Performs parallel calculations with bootstrapping for statistical analysis.
- Outputs results in JSON format for further analysis.

## Requirements

- Python 3.8 or higher
- Required Python packages (install via `requirements.txt` if available):
  - `argparse`
  - Custom modules from the project:
    - `variation_project.utils.alignment_parsing`
    - `variation_project.core.process_indels`
    - `variation_project.core.calculate`
    - `variation_project.utils.record_out`

## Usage

Run the script using the following command syntax from the command line:

```bash
python -m variation_project <gene> <level> <top_sample_number> <directory> <output>
```

### Positional Arguments
gene: The gene to analyze (e.g., A).
level: The level of analysis. Choose from:
nuc: Nucleotide level
prot: Protein level
gen: Genomic level
top_sample_number: The highest sample number to analyze. The script will process all sample sizes up to this number, starting from 50.
directory: The directory containing the alignment files.
output: The directory where the output files will be saved.
Example

```bash
python -m variation_project A nuc 500 ./data ./output
```

This command will:
Analyze the HLA-A gene at the nucleotide level.
Process sample sizes from 50 to 500.
Save the output JSON files in the ./output directory.

## Output
The script generates JSON files for each combination of sample size and bootstrap iteration. The files are saved in the specified output directory with the naming convention:

`<gene>_<sample_size>_<bootstrap>.json`

Examples:
`A_50_50.json`
`A_100_60.json`

## Contact
For questions or feedback, please contact Sebastian Hopper.
