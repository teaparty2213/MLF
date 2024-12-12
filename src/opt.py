# O(2^K*s) time exact algorithm for heterozygous phasing (K: max coverage, s: number of SNP positions)

from open_input_file import read_file
from gray_code import gray_code, gray_code_dif_bit, get_Nth_bit
from enum import Enum
import numpy as np

def read_range(r, s, M): # calculate the range of read index at each site
    read_range_list = []
    first = 0
    last = 0
    for j in range(s):
        i = 0
        while (i < r and M[i][j] == -1):
            i += 1
        first = i
        while (i < r and M[i][j] != -1):
            i += 1
        last = i - 1
        read_range_list.append((first, last))
    return read_range_list

def max_coverage(read_range_list):
    max_coverage = 0
    for i in range(len(read_range_list)):
        max_coverage = max(max_coverage, read_range_list[i][1] - read_range_list[i][0] + 1)
    return max_coverage

def count_allele(M, j, first, last, gray): # count the number of 0s and 1s in Group X and Y at site j
    count = [0, 0, 0, 0] # count[0]: #0 in X, count[1]: #1 in X, count[2]: #0 in Y, count[3]: #1 in Y
    bit_shift = 0
    for i in range(first, last + 1):
        group = (gray >> bit_shift) & 1 # group of read i (represented by 0 or 1)
        if (group == 0):
            if (M[i][j] == 0):
                count[0] += 1
            elif (M[i][j] == 1):
                count[1] += 1
        elif (group == 1):
            if (M[i][j] == 0):
                count[2] += 1
            elif (M[i][j] == 1):
                count[3] += 1
        bit_shift += 1
    return count

def opt_algo()

def main(path):
    r, s, M = read_file(path)
    read_range_list = read_range(r, s, M)
    K = max_coverage(read_range_list)
    
    c = count_allele(M, 4, 0, 4, 0b10101)
    print(c)

main('../data/input_1.txt')