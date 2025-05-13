"""Script containing function to calculate number of differing positions"""

def pairwise_difference(seq1, seq2):
    """Calculates the number of differing positions, is an implementation of the hamming distance (assumes equal length)""" #pylint: disable=line-too-long
    return sum(a != b for a,b in zip(seq1, seq2))
