# generate random data (allele matrix)

from read_range import read_range
from max_coverage import max_coverage
from build_graph import build_graph
import random
import numpy as np
import networkx as nx

def random_gen(read_num, N):
    r = random.randint(read_num - read_num // 10, read_num + read_num // 10)
    s = r
    min_range = read_num // 5
    
    M = []
    start_idx = 0
    end_idx = min_range - 1
    for i in range(r):
        row = [-1] * s
        if (i > 1):
            start_idx = start_idx + np.random.choice([0, 1])
            end_idx = max(start_idx + min_range, end_idx + np.random.choice([0, 1]))
            if (end_idx >= s):
                end_idx = s - 1
        non_negative_len = end_idx - start_idx + 1
        non_negative_values = list(np.random.randint(0, N, size=non_negative_len))
        row[start_idx : start_idx + non_negative_len] = non_negative_values
        M.append(row)
    
    # check if there is a column with all -1
    valid_columns = []
    del_column_count = 0
    for j in range(s):
        all_negative = True
        for i in range(r):
            if (M[i][j] != -1):
                valid_columns.append(j)
                all_negative = False
                break
        if all_negative:
            del_column_count += 1
    s -= del_column_count
    new_M = [[M[i][j] for j in valid_columns] for i in range(r)]
            
    return r, s, new_M

def gen_planar_data(read_num): # 変数Nに非対応(未実装)
    non_planar = True
    while (non_planar):
        r, s, M = random_gen(read_num)
        K = 25
        
        # check if the maximum coverage of M is less than K
        read_range_list = read_range(r, s, M)
        max_cov = max_coverage(read_range_list)
        
        # check if the graph is planar
        G = build_graph(r, s, M)
        is_planar, embedding = nx.check_planarity(G, counterexample=False)
        
        if (max_cov < K and is_planar):
            non_planar = False # planar data is generated
    return r, s, M

def gen_non_planar_data(read_num, N):
    cov_cond = True
    while (cov_cond):
        r, s, M = random_gen(read_num, N)
        K = 0
        if N == 2:
            K = 24
        elif N == 3:
            K = 15
        elif N == 4:
            K = 12
        
        # check if the maximum coverage of M is less than K
        read_range_list = read_range(r, s, M)
        max_cov = max_coverage(read_range_list)
        if (max_cov <= K):
            cov_cond = False

    return r, s, M

def main_planar(path, file_num, read_num): # 変数Nに非対応(未実装)
    # generate random planar data
    for i in range(1, file_num + 1):
        r, s, M = gen_planar_data(read_num)
        file = '{}/input_'.format(path) + str(i) + '.txt'
        with open(file, 'w') as f:
            f.write(str(r) + '\n')
            f.write(str(s) + '\n')
            for row in M:
                f.write(''.join(['-' if char == -1 else str(char) for char in row]) + '\n')
                
def main_non_planar(path, file_num, read_num, N): # N: the number of haplotypes
    # generate random non planar data
    for i in range(1, file_num + 1):
        r, s, M = gen_non_planar_data(read_num, N)
        file = '{}/input_'.format(path) + str(i) + '.txt'
        with open(file, 'w') as f:
            f.write(str(r) + '\n')
            f.write(str(s) + '\n')
            for row in M:
                f.write(''.join(['-' if char == -1 else str(char) for char in row]) + '\n')

main_non_planar('../data/tetraploid', 10, 24, 2)
#main_planar('../data/planar_data', 10, 18) # N=2だとread_numは18ぐらいが限界で，それ以上だとplanarなグラフが全く生成できない