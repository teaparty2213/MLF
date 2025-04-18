# Input file must be in the format below:
    # every two reads are continuous
    # reads that are not sequenced at every SNP are not permitted
    # SNP positions include at least one read
import numpy as np

def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    r = int(lines[0].strip()) # number of reads
    s = int(lines[1].strip()) # number of SNP positions
    M = np.zeros((r, s), dtype=int) # allele matrix
    
    max_num = 0 # ploidy - 1
    for i, line in enumerate(lines[2:]):
        row = [int(char) if char.isdigit() else -1 for char in line.strip()] # -1 for - (not sequenced data)
        max_num = max(max_num, max(row))
        M[i, :len(row)] = row
        
    return r, s, M, max_num + 1