##-------------------------------------------------------------
## Reference: Genome-Scale Algorithm Design 2nd edition, Chapter 14: Haplotype analysis
## O(2^K*s) time exact algorithm for haplotype phasing (K: max coverage, s: number of SNP positions)
## Left to do: implement traceback to find the optimal bipartition
## Special thanks to Tomoyuki Unno for helping implement
##-------------------------------------------------------------
from gray_code import gray_code, gray_code_dif_bit, get_Nth_bit
import numpy as np
import time

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

def opt_for_diploid(r, s, M, read_range_list, K): # O(2^K*s) time exact algorithm for phasing
    max_states = 2 ** K
    D = [[r * s] * max_states for i in range(s)] # DP table for the minimum number of errors (column: site, row: gray_code)
    shared_D = [r * s] * max_states # current minimum number of errors
    pre_shared_D = [r * s] * max_states # previous minimum number of errors
    
    # initialize DP table (j = 0)
    first = read_range_list[0][0]
    last = read_range_list[0][1]
    width = last - first + 1
    next_first = read_range_list[1][0]
    next_shared_width = last - next_first + 1
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
        shared_idx = (gray >> (width - next_shared_width)) & ((1 << next_shared_width) - 1) # digits used in the next site
        shared_D[shared_idx] = min(shared_D[shared_idx], D[0][gray])
    
    # recursion
    min_D = r * s
    for j in range(1, s):
        first = read_range_list[j][0]
        last = read_range_list[j][1]
        width = last - first + 1
        pre_shared_width = next_shared_width
        pre_shared_mask = (1 << pre_shared_width) - 1
        if (j < s - 1):
            next_first = read_range_list[j + 1][0]
            next_shared_width = last - next_first + 1
        count = count_allele(M, j, first, last, 0) # gray_code = 0
        min_flip = min(count[0], count[1]) + min(count[2], count[3])
        
        for i in range(1, 2 ** width): # i: gray_code
            gray = gray_code(i)
            pre_gray = gray_code(i - 1)
            dif_bit = gray_code_dif_bit(gray, pre_gray)
            
            if (get_Nth_bit(gray, dif_bit) == 0): # Group of read[first + dif_bit] changes from Y to X
                if (M[first + dif_bit][j] == 0): # #0 in X increases by 1, #0 in Y decreases by 1
                    count[0] += 1
                    count[2] -= 1
                elif (M[first + dif_bit][j] == 1): # #1 in X increases by 1, #1 in Y decreases by 1
                    count[1] += 1
                    count[3] -= 1
            elif (get_Nth_bit(gray, dif_bit) == 1): # Group if read[first + dif_bit] changes from X to Y
                if (M[first + dif_bit][j] == 0): # #0 in X decreases by 1, #0 in Y increases by 1
                    count[0] -= 1
                    count[2] += 1
                elif (M[first + dif_bit][j] == 1): # #1 in X decreases by 1, #1 in Y increases by 1
                    count[1] -= 1
                    count[3] += 1
            
            min_flip = min(count[0], count[1]) + min(count[2], count[3])
            D[j][gray] = shared_D[gray & pre_shared_mask] + min_flip
            if (j < s - 1):
                shared_idx = (gray >> (width - next_shared_width)) & ((1 << next_shared_width) - 1) # digits used in the next site
                pre_shared_D[shared_idx] = min(pre_shared_D[shared_idx], D[j][gray])
            else: # j = s - 1 (last column)
                min_D = min(min_D, D[j][gray])
                
        shared_D = pre_shared_D.copy()
        pre_shared_D = [r * s] * max_states
    return min_D
