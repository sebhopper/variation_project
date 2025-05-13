"""Subsampling script"""

#Standard Imports
import random

def subsample(alignment, n):
    """Function to subsample from the alignment"""
    return dict(random.sample(list(alignment.items()), n))
