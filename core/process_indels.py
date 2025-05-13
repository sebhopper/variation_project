"""Script containing functions to process indels"""

#Standard Imports
import re

def process_indels(alleles):
    """Function to process indels per allele in an alignment"""
    refseq = next(iter(alleles.values()))
    for i, _ in enumerate(refseq):
        if refseq[i] == ".":
            refseq = refseq[:i] + "!" + refseq[i + 1 :]
            for allele, allele_seq in alleles.items():
                seqbase = allele_seq[i]
                if seqbase == ".":
                    alleles[allele] = allele_seq[:i] + "!" + allele_seq[i + 1 :]
                elif re.search(r"[ACTGX]", seqbase):
                    alleles[allele] = allele_seq[:i] + "I" + allele_seq[i + 1 :]
    for allele, allele_seq in alleles.items():
        allele_seq = re.sub(r"I{1,}[ACGTX]", "I", allele_seq)
        alleles[allele] = allele_seq.replace(".", "D").replace("!", "")

    return alleles
