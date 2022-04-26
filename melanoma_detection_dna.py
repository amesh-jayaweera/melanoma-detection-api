from fuzzywuzzy import ratio
import math
import numpy as np
import pandas as pd
import itertools
from strsimpy.normalized_levenshtein import NormalizedLevenshtein


def detect_mutations(age, patient_dna, gene_name):
    gene = get_gene_seq(gene_name, 'cdna')
    threshold = calculate_similarity_threshold(gene, age)
    is_within_threshold = is_similarity_within_threshold(patient_dna, gene, threshold)
    if not is_within_threshold:
        print(" ======= ")
        defragmented_patient_dna = defragment_patient_dna(gene, patient_dna, threshold, gene_name)
        mutations, mutation_positions = find_mutations(defragmented_patient_dna, gene)
        return mutations, mutation_positions
    else:
        mutations, mutation_positions = find_mutations(patient_dna, gene)
        return mutations, mutation_positions


def get_gene_seq(gene_name, _type):
    file_name = 'data/ref-gene-seq/ref-gene-' + gene_name.lower() + '.txt'
    print(file_name)
    file = open(file_name, 'r')
    sequence = file.read()
    file.close()
    return sequence


def calculate_similarity_threshold(gene, age):
    nucleotides = len(gene)
    mutation_percentage = round(238 * 100 / nucleotides, 2)

    if mutation_percentage < 10:
        print('Original mutation percentage:', mutation_percentage)
        if math.isnan(age):
            print('Age is NaN')
        if age > 20:
            mutation_percentage = mutation_percentage * 1.5
        if age > 40:
            mutation_percentage = mutation_percentage * 2.11
        if age > 60:
            mutation_percentage = mutation_percentage * 1.5
        if age > 80:
            mutation_percentage = mutation_percentage * 1.4

    return 100 - mutation_percentage


def is_similarity_within_threshold(patient_dna, gene, threshold):
    _ratio = ratio(gene, patient_dna)

    is_within_threshold = False
    if _ratio > threshold:
        is_within_threshold = True

    return is_within_threshold


######################
# Defragmentation algorithm

def defragment_patient_dna(gene, patient_dna, threshold, gene_name):
    probability_array = setup_defragmentation_algo(gene, patient_dna, gene_name)
    new_ratio = ratio(gene, patient_dna)
    defragmented_patient_dna = patient_dna
    normalized_levenshtein = NormalizedLevenshtein()

    while new_ratio < threshold:
        min_probability = min(probability_array[2])
        col_index = probability_array[2].index(min_probability)
        if min_probability < 0.0001:
            new_ratio = ratio(gene, defragmented_patient_dna)
        elif min_probability < 0.5:
            new_strsimpy_ratio = normalized_levenshtein.distance(gene, defragmented_patient_dna) * 100
            new_ratio = 100 - new_strsimpy_ratio

        probability_array[1][col_index] = probability_array[0][col_index]
        probability_array[2][col_index] = 1
        defragmented_patient_dna = "".join(probability_array[1])

    return defragmented_patient_dna


def setup_defragmentation_algo(gene, patient_dna, gene_name):
    rows = 3
    cols = len(gene)
    probability_array = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(len(gene)):
        probability_array[0][i] = gene[i]
        probability_array[1][i] = patient_dna[i]
        probability_array[2][i] = 0

    actual_mutated = pd.read_csv('data/mutated_genes.csv', delimiter=',')
    random_mutations = actual_mutated[actual_mutated['GENE'].isin([gene_name])].sample(frac=0.8).reset_index(drop=True)

    _matrix = [[0 for _ in range(cols)] for _ in range(len(random_mutations))]

    for row in range(len(random_mutations)):
        sample = random_mutations.iloc[row]['MUTATED_SEQ']
        for i in range(len(sample)):
            _matrix[row][i] = sample[i]

    i = 0
    while i in range(len(gene)):
        patient_nucleotide = probability_array[1][i]
        if probability_array[0][i] == patient_nucleotide:
            probability_array[2][i] = 1
        else:
            count = 0
            for j in range(len(random_mutations)):
                if patient_nucleotide == _matrix[j][i]:
                    count += 1
            probability = count / len(random_mutations)
            probability_array[2][i] = probability
        i += 1

    return probability_array


######################
# Smith Waterman Algorithm implementation

def matrix(a, b, match_score=3, mismatch_score=-3, gap_cost=2):
    #     initialize the 2D array and fill with zeros
    H = np.zeros((len(a) + 1, len(b) + 1), np.int)

    #     finding the candidate diagonal, left, and up values
    for i, j in itertools.product(range(1, H.shape[0]), range(1, H.shape[1])):
        diagonal = H[i - 1, j - 1] + (match_score if a[i - 1] == b[j - 1] else mismatch_score)
        left = H[i - 1, j] - gap_cost
        up = H[i, j - 1] - gap_cost
        H[i, j] = max(diagonal, left, up, 0)
    return H


def traceback(H, b, b_='', old_i=0):
    # flip H to get index of **last** occurrence of H.max() with np.argmax()
    H_flip = np.flip(np.flip(H, 0), 1)
    i_, j_ = np.unravel_index(H_flip.argmax(), H_flip.shape)
    i, j = np.subtract(H.shape, (i_ + 1, j_ + 1))  # (i, j) are the **last** indices of H.max()
    if H[i, j] == 0:  # recursion break point
        return b_, j
    b_ = b[j - 1] + '-' + b_ if old_i - i > 1 else b[
                                                       j - 1] + b_  # inserting a gap if backtracking in the same
    # direction
    return traceback(H[0:i, 0:j], b, b_, i)


def smith_waterman(a, b, match_score=3, mismatch_score=-3, gap_cost=2):
    a, b = a.upper(), b.upper()
    H = matrix(a, b, match_score, mismatch_score, gap_cost)
    b_, pos = traceback(H, b)
    return pos, pos + len(b_)


def difference(str1, str2):
    diff = []
    for a, b in zip(str1, str2):
        if a != b:
            diff.append(a + ' > ' + b)
    return diff


def find_mutations(defragmented_patient_dna, gene):
    mutations = difference(gene, defragmented_patient_dna)
    mutation_positions = [i + 1 for i in range(len(gene)) if gene[i] != defragmented_patient_dna[i]]
    return mutations, mutation_positions
