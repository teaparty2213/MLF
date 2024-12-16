# generate random data (allele matrix)

from read_range import read_range
from max_coverage import max_coverage
from build_graph import build_graph
import random
import numpy as np
import networkx as nx

def random_gen():
    r = random.randint(30, 40)
    s = r
    min_range = 5
    
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
        non_negative_values = np.random.choice([0, 1], non_negative_len)
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

def gen_planar_data():
    non_planar = True
    while (non_planar):
        r, s, M = random_gen()
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

def gen_data(path):
    # generate 5 random planar data
    for i in range(1, 6):
        r, s, M = gen_planar_data()
        file = '{}/input_'.format(path) + str(i) + '.txt'
        with open(file, 'w') as f:
            f.write(str(r) + '\n')
            f.write(str(s) + '\n')
            for row in M:
                f.write(''.join(['-' if char == -1 else str(char) for char in row]) + '\n')
                
gen_data('../data/planar_data')