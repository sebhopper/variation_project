"""Script to complete calculations"""

#Standard Imports
import statistics as stats
from concurrent.futures import ProcessPoolExecutor, as_completed
from alive_progress import alive_bar

#Specialist Imports
import Levenshtein as lev

#Project imports
from core.subsampling import subsample
from core.pairwise_calculation import pairwise_difference

def calculate(alignment, sub_sample_size, bootstrap_number):
    """Single entry point for sub-sampling, bootstrapping """
    results = []
    # steps = range(0, 10000, 10)
    with alive_bar(bootstrap_number, bar = 'classic2', spinner = 'dots') as progress_bar:
        for _ in range(bootstrap_number):
            #Resample with replacement
            sequences = subsample(alignment, sub_sample_size)
            subsample_result = within_subsample_distances(sequences)
            results.append(total_subsample_results(subsample_result))
            progress_bar() #pylint: disable=not-callable

    return results

def parallel_calculate(alignment, sub_sample_size, bootstrap_number, num_workers=4):
    """Run the calculate function in parallel using multiple processes."""
    # Split the bootstrap iterations into chunks for parallel processing
    chunk_size = bootstrap_number // num_workers
    futures = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for _ in range(num_workers):
            futures.append(
                executor.submit(calculate, alignment, sub_sample_size, chunk_size)
            )

        results = []
        for future in as_completed(futures):
            results.extend(future.result())

    return results

def within_subsample_distances(sequences):
    """Calculate total distances between alleles within the sample"""
    subsample_results = []
    for i, (allele1, sequence1) in enumerate(sequences.items()):
        for allele2, sequence2 in list(sequences.items())[i+1:]:
            subsample_results.append({
                'allele1': allele1,
                'allele2': allele2,
                'pairwise_difference': pairwise_difference(sequence1, sequence2),
                'levenshtein_distance': lev.distance(sequence1, sequence2)
            })

    return subsample_results

def total_subsample_results(subsample_results):
    """Produce dictionary containing stats for the whole subsample"""

    pairdist_comparisons = [comparison['pairwise_difference'] for comparison in subsample_results]
    levdist_comparisons = [comparison['levenshtein_distance'] for comparison in subsample_results]

    results = {'pairdist_mean': stats.mean(pairdist_comparisons),
               'pairdist_stdev': stats.stdev(pairdist_comparisons),
               'pairdist_var': stats.variance(pairdist_comparisons),
               'levdist_mean': stats.mean(levdist_comparisons),
               'levdist_stdev': stats.stdev(levdist_comparisons),
               'levdist_var': stats.variance(levdist_comparisons)}

    return results
