# haplotype phasing for N-ploid organisms
from open_input_file import read_file
from read_range import read_range
from max_coverage import max_coverage
from opt import opt_for_diploid
from build_graph import build_graph
from color_annealing import color_annealing
from open_file_for_polyploid import read_file_of_polyploid
from rand_index import rand_index
from reconstruct_hap import recostruct_haplotype
from sklearn.metrics.cluster import adjusted_rand_score
import numpy as np
import time
import matplotlib.pyplot as plt
import networkx as nx
import statistics
import math

def main(path):
    '''
    r, s, M, N = read_file(path)
    # exact algorithm
    read_range_list = read_range(r, s, M)
    K = max_coverage(read_range_list)
    min_D = opt_for_diploid(r, s, M, read_range_list, K)
    '''
    
    for path in data:
        N, r, s, M, err_num, ans_list, haplotypes = read_file_of_polyploid(path)
        print("N: ", N)
        
        # heuristic
        app_set = []
        ARI_set = []
        OPT = 0
        
        for i in range(0, 1):
            start = time.perf_counter()
            G, H, I = build_graph(r, s, M, read_share_ratio=0.8)
            cost, color, cost_history = color_annealing(r, s, N, G, H, I, ans_list, alpha=0.9, neighbor_rate=0.1)
            end = time.perf_counter()
            time2 = end - start
            
            # calculate OPT
            if i == 0:
                for e in I.edges():
                    if ans_list[e[0]] == ans_list[e[1]]:
                        OPT += I[e[0]][e[1]]['weight']
                    
            ARI = adjusted_rand_score(ans_list, color)
            app_set.append(cost / OPT)
            ARI_set.append(ARI)
            
            if i == 0:
                iteration = list(range(0, len(cost_history)))
                plt.figure()
                plt.plot(iteration, cost_history, label="cost")
                plt.plot([0, len(cost_history)], [OPT, OPT], color='red', label="answer")
                plt.xlabel("iteration")
                plt.ylabel("cost")
                plt.title("number of errors in {}-ploid".format(N))
                plt.legend(loc="upper right")
                #plt.savefig("./../result/250124_{}-ploid.png".format(N))
                
                recostruct_haplotype(r, s, N, M, color, haplotypes)
        
        app_e = statistics.mean(app_set)
        app_v = statistics.variance(app_set)
        ARI_e = statistics.mean(ARI_set)
        ARI_v = statistics.variance(ARI_set)
        
        print("OPT: ", OPT)
        print("average approximation error: ", app_e)
        print("variance of approximation error: ", app_v)
        print("average ARI: ", ARI_e)
        print("variance of ARI: ", ARI_v)

data = ['../data/polyploid/input_0.txt', '../data/polyploid/input_1.txt', '../data/polyploid/input_2.txt']
main(data)