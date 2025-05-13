"""Main module"""

#Standard imports
import argparse
from pathlib import Path
from datetime import datetime

#Project imports
from variation_project.utils.alignment_parsing import IPDAlignment
from variation_project.core.process_indels import process_indels
from variation_project.core.calculate import parallel_calculate, calculate
from variation_project.utils.record_out import create_output_folder, write_json_file

def main():

    args = get_args()

    filehandle = Path(f"{args.directory}/{args.gene.title()}_{args.level}.txt")

    alignment = IPDAlignment(filehandle)

    #If class I being analysed use this block
    exon2_3_alignment = alignment.exon2_3_alignment()
    processed_alignment = process_indels(exon2_3_alignment)

    #If class II being analysed use this block
    # exon2_alignment = alignment.exon2_alignment()
    # processed_alignment = process_indels(exon2_alignment)

    #Create the output directory
    date_str = datetime.now().strftime("%Y-%m-%d")
    output_location = create_output_folder(args.output, f'{args.gene}_{args.level}_{args.top_sample_number}_{date_str}')

    #Set the range for the number of sequences to sample
    no_seqs = range(50, int(args.top_sample_number)+1, 50)
    #Set the range for the number of bootstraps
    bootstrap_range = range(50,1000+1, 10)

    #Begin calculation loop
    for bootstrap in bootstrap_range:
        for sample_size in no_seqs:
            results = parallel_calculate(processed_alignment, sample_size, bootstrap)
            write_json_file(results, output_location, f"{args.gene}_{sample_size}_{bootstrap}.json")


def get_args():
    """Create the Argument Parser"""

    #Construct the argument parser
    parser = argparse.ArgumentParser()

    parser.add_argument('gene',
                        help="Gene to analyse")

    parser.add_argument('level',
                        choices=['nuc', 'prot', 'gen'],
                        help="Level to analyse")

    parser.add_argument('top_sample_number',
                        default= 5,
                        help='The highest sample number, script will complete all up to this level from 5') #pylint: disable=line-too-long

    parser.add_argument('directory',
                        help='Directory containing the alignments')

    parser.add_argument('output',
                        help='Location of directory output')

    return parser.parse_args()


if __name__ == '__main__':
    main()
