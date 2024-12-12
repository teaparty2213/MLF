# O(2^K*s) time exact algorithm for heterozygous phasing (K: max coverage, s: number of SNP positions)

from open_input_file import read_file
from gray_code import gray_code, gray_code_dif_bit, get_Nth_bit
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
        group = (gray >> bit_shift) & 1 # group of read i (represented by 0(X) or 1(Y))
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

def opt_algo(r, s, M, read_range_list, K): # O(2^K*s) time exact algorithm for heterozygous phasing
    max_states = 2 ** K
    D = [[r * s] * max_states for i in range(s)] # DP table for the minimum number of errors (column: site, row: gray_code)
    shared_D = [r * s] * max_states # current minimum number of errors
    pre_shared_D = [r * s] * max_states # previous minimum number of errors
    
    # initialize DP table (j = 0)
    first = read_range_list[0][0]
    last = read_range_list[0][1]
    width = last - first + 1
    next_first = read_range_list[1][0]
    shared_width = last - next_first + 1
    count = count_allele(M, 0, first, last, 0) # gray_code = 0
    min_flip = min(count[0], count[1]) + min(count[2], count[3])
    for i in range(1, 2 ** width): # i: gray_code
        gray = gray_code(i)
        pre_gray = gray_code(i - 1)
        dif_bit = gray_code_dif_bit(gray, pre_gray)

        if (get_Nth_bit(gray, dif_bit) == 0): # Group of read[first + dif_bit] changes from Y to X
            if (M[first + dif_bit][0] == 0): # #0 in X increases by 1, #0 in Y decreases by 1
                count[0] += 1
                count[2] -= 1
            elif (M[first + dif_bit][0] == 1): # #1 in X increases by 1, #1 in Y decreases by 1
                count[1] += 1
                count[3] -= 1
        elif (get_Nth_bit(gray, dif_bit) == 1): # Group if read[first + dif_bit] changes from X to Y
            if (M[first + dif_bit][0] == 0): # #0 in X decreases by 1, #0 in Y increases by 1
                count[0] -= 1
                count[2] += 1
            elif (M[first + dif_bit][0] == 1): # #1 in X decreases by 1, #1 in Y increases by 1
                count[1] -= 1
                count[3] += 1
                
        min_flip = min(count[0], count[1]) + min(count[2], count[3])
        D[0][gray] = min_flip
        shared_idx = (gray >> (width - shared_width)) & ((1 << shared_width) - 1) # digits used in the next site
        shared_D[shared_idx] = min(shared_D[shared_idx], D[0][gray])
                

def main(path):
    r, s, M = read_file(path)
    read_range_list = read_range(r, s, M)
    K = max_coverage(read_range_list)
    opt_algo(r, s, M, read_range_list, K)

main('../data/input_1.txt')