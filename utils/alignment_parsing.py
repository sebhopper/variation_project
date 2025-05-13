"""Script with functions to parse the IPD-IMGT/HLA alignment txt files"""
#Standard imports
from typing import TextIO
import re
from pathlib import Path

#Define Regex for allele names
ALLELE_NAME_REGEX = re.compile(r'([A-Za-z1-9]+\*(?:\d+:?)+\d+[NSQL]?)')

def parse_alignments(alignment_filepath):
    """Function to parse the alignment txt file"""
    with open(alignment_filepath, 'r', encoding='utf-8') as file:
        return read_alignment(file)

def read_alignment(file:TextIO):
    """Read the alignment from file and return a reformatted dict of aligned alleles"""

    while next(file).startswith('#'):
        continue

    alignment = {}

    for line in file:
        if not ALLELE_NAME_REGEX.search(line):
            continue

        line = re.split(r'[\t ]+', line.strip())

        if (allele_name := line[0]) not in alignment:
            alignment[allele_name] = ''

        alignment[allele_name] += ''.join(line[1:])

        for allele_name, sequence in alignment.items():
            if '-' not in sequence:
                reference = allele_name
                break

    formatted_alignment = reformat_alignment(alignment, reference)
    removed_pipes_alignment = remove_pipes(formatted_alignment)

    return removed_pipes_alignment

def reformat_alignment(alignment:dict, reference:str):
    """Reformat the alignment to replace '-' with the sequence from the reference"""

    for allele_name, sequence in alignment.items():
        if allele_name == reference:
            continue

        alignment[allele_name] = ''.join(
            ref if seq == '-' else seq
            for ref, seq in zip(alignment[reference], sequence))

    return alignment

def remove_pipes(alignment:dict):
    """Remove pipes from alignment"""
    no_pipes_alignment = {allele_name: sequence.replace('|','')
                          for allele_name, sequence in alignment.items()}

    return no_pipes_alignment


class IPDAlignment:
    """Class implementation of parsing IPD-IMGT/HLA alignment files"""
    def __init__(self, filepath:Path):
        self.filepath = filepath
        self.alignment = {}
        self.reference = None

        with open(self.filepath, 'r', encoding='utf-8') as file:
            self.read_alignment(file)
            self.reformat_alignment()

    def read_alignment(self, file:TextIO):
        """Read and extract alignment information from the file."""

        #Skip over metadata lines at the top of the file
        while next(file).startswith('#'):
            continue

        for line in file:
            if not ALLELE_NAME_REGEX.search(line):
                continue

            line = re.split(r'[\t ]+', line.strip())

            allele_name = line[0]

            if allele_name not in self.alignment:
                self.alignment[allele_name] = ''

            self.alignment[allele_name] += ''.join(line[1:])

        #Determine the reference allele (first sequence without '-')
        for allele_name, sequence in self.alignment.items():
            if '-' not in sequence:
                self.reference = allele_name
                break

    def reformat_alignment(self):
        """Reformat the alignment to replace '-' with sequence from the reference"""

        reference_seq = self.alignment[self.reference]
        for allele_name, sequence in self.alignment.items():

            if allele_name == self.reference:
                continue

            self.alignment[allele_name] = ''.join(
                ref if seq == '-' else seq
                for ref, seq in zip(reference_seq, sequence)
            )

    def get_alignment(self):
        """Return the final processed alignment dictionary."""
        return self.alignment

    def remove_pipes(self):
        """Remove pipes from alignment"""
        self.alignment = {allele_name: sequence.replace('|','')
                          for allele_name, sequence in self.alignment.items()}

    def exon2_alignment(self):
        """Use pipes to get the exon 2 sequence"""
        level = self.filepath.stem.split('_')[1]
        exon2_alignment = {}

        for allele, sequence in self.alignment.items():
            feature_sequences = sequence.split('|')

            if level == 'gen':
                exon2_alignment[allele] = feature_sequences[3]

            if level == 'nuc':
                exon2_alignment[allele] = feature_sequences[2]

        return exon2_alignment

    def exon2_3_alignment(self):
        """Use pipes to get the exon 2 and 3 sequence"""
        level = self.filepath.stem.split('_')[1]
        exon2_3_alignment = {}

        for allele, sequence in self.alignment.items():
            feature_sequences = sequence.split('|')

            if level == 'gen':
                exon2_3_alignment[allele] = feature_sequences[3] + feature_sequences[5]

            if level == 'nuc':
                exon2_3_alignment[allele] = feature_sequences[1] + feature_sequences[2]

        return exon2_3_alignment
