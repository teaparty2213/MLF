# Input file must be in the format below:
    # every two reads are continuous
    # reads that are not sequenced at every SNP are not permitted
    # SNP positions include at least one read
import numpy as np

def read_file_of_polyploid(file):
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    N = int(lines[0].strip()) # ploidy
    r = int(lines[1].strip()) # number of reads
    s = int(lines[2].strip()) # number of SNP positions
    
    M = np.zeros((r, s), dtype=int) # allele matrix
    for i, line in enumerate(lines[3:3+r]):
        row = [int(char) if char.isdigit() else -1 for char in line.strip()] # -1 for - (not sequenced data)
        M[i, :len(row)] = row

    err_num = int(lines[3+r].strip()) # number of errors
    ans_list = list(map(int, lines[4+r].strip().split())) # haplotype list
    haplotypes = []
    for i in range(N):
        hap = list(map(int, lines[5+r+i].strip()))
        haplotypes.append(hap)
        
    return N, r, s, M, err_num, ans_list, haplotypes