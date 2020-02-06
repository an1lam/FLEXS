import os
import itertools
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sys
sys.path.append("../")
from models.Ground_truth_oracles.RNA_landscape_models import RNA_landscape_constructor
from models.Ground_truth_oracles.TF_binding_landscape_models import *
import multiprocessing 
print('Number of CPUs', multiprocessing.cpu_count())

def is_sequence_a_peak(model, sequence, peak_dict, alphabet="AGTC"):
    if sequence in peak_dict:
        return peak_dict[sequence]
    neighbor=[s for s in sequence]
    sequence_fitness=model.get_fitness(sequence)
    for position in range(len(sequence)):
        for aa in alphabet:
            if aa!=sequence[position]:
               neighbor[position]=aa
               neighbor_string="".join(neighbor)
               if sequence_fitness<model.get_fitness(neighbor_string):
                  peak_dict[sequence] = 0
                  return 0
               elif sequence_fitness>model.get_fitness(neighbor_string):
                  peak_dict[neighbor_string] = 0
               neighbor[position]=sequence[position] # reset 
    peak_dict[sequence] = 1
    return 1

def get_peaks_subset(start_subset, model, alphabet):
    peaks=set()
    peak_dict = {}
    for ind, sub_seq in enumerate(itertools.product(alphabet, repeat=11)):
        seq = start_subset + sub_seq
        if ind % 100000 == 0:
            print('Processed {} sequences and found {} peaks in processing sequences starting with {}'.format(ind, len(peaks), start_subset))
        seq = ''.join(seq)
        if is_sequence_a_peak(model, seq, peak_dict, alphabet):
           peaks.add(seq)
    return peaks

def get_all_peaks(landscape, alphabet='AGTC'):
    # we will be running 4^3 = 64 processes, so each individual function will be running on sequences that start with the same XYZ
    pool = multiprocessing.Pool(64)
    start_subset_seqs = itertools.product(alphabet, repeat=3)
    args = [(subset_seq, landscape, alphabet) for subset_seq in start_subset_seqs]
    all_found_peaks = pool.starmap(get_peaks_subset, args)
    peaks = set()
    for peak_subset in all_found_peaks:
        peaks.update(peak_subset)
    peaks = list(peaks)
    return peaks

if not os.path.isdir('../peaks'):
    os.mkdir('../peaks')
    
rna_landscape_constructor_1=RNA_landscape_constructor()
rna_landscape_constructor_1.load_landscapes("../data/RNA_landscapes/RNA_landscape_config.yaml", 
                                      landscapes_to_test = [0])
landscape1 = next(rna_landscape_constructor_1.generate_from_loaded_landscapes())
rna_landscape_constructor_2=RNA_landscape_constructor()
rna_landscape_constructor_2.load_landscapes("../data/RNA_landscapes/RNA_landscape_config.yaml", 
                                      landscapes_to_test = [12])
landscape2 = next(rna_landscape_constructor_2.generate_from_loaded_landscapes())

peaks_2 = get_all_peaks(rna_landscape_constructor_2["landscape_oracle"], 'UGTC')
pickle.dump(peaks_2, open('../peaks/peaks_B2L14RNA1+2.pkl', 'wb'))