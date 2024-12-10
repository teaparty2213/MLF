import numpy as np

def read_file(file):
    with open(file, 'r') as f:
        lines = f.readlines()
    r = int(lines[0].strip()) # number of reads
    s = int(lines[1].strip()) # number of SNP positions
    M = np.zeros((r, s), dtype=int) # allele matrix
    
    for i, line in enumerate(lines[2:]):
        row = [int(char) if char.isdigit() else -1 for char in line.strip()] # -1 for - (not sequenced data)
        M[i, :len(row)] = row
        
    return r, s, M