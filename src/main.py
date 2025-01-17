# haplotype phasing for N-ploid organisms
from open_input_file import read_file
from read_range import read_range
from max_coverage import max_coverage
from opt import opt_for_diploid
from build_graph import build_graph
from color_annealing import color_annealing
from open_file_for_polyploid import read_file_of_polyploid
from rand_index import rand_index
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
    start = time.perf_counter()
    read_range_list = read_range(r, s, M)
    K = max_coverage(read_range_list)
    min_D = opt_for_diploid(r, s, M, read_range_list, K)
    end = time.perf_counter()
    time1 = end -start
    '''
    
    for path in data:
        N, r, s, M, err_num, ans_list, haplotypes = read_file_of_polyploid(path)
        print("N: ", N)
        
        # heuristic
        app_set = []
        time_set = []
        for i in range(0, 50):
            start = time.perf_counter()
            G, H, I = build_graph(r, s, M, read_share_ratio=0.8)
            nx.draw(G)
            plt.show()
            cost, color, cost_history = color_annealing(r, s, N, G, H, I, alpha=0.9, neighbor_rate=0.1)
            end = time.perf_counter()
            time2 = end - start
            
            app_set.append(cost / err_num)
            time_set.append(time2)
            
            if i == 0:
                ARI = rand_index(ans_list, color, 0, r - 1, N)
                print("ARI: ", ARI)
                
                iteration = list(range(0, len(cost_history)))
                plt.figure()
                plt.plot(iteration, cost_history)
                plt.plot([0, len(cost_history)], [err_num, err_num], color='red')
                plt.xlabel("iteration")
                plt.ylabel("cost")
                plt.title("number of errors in {}-ploid".format(N))
                plt.savefig("./../result/250117_{}-ploid.png".format(N))
        
        app_e = statistics.mean(app_set)
        app_v = statistics.variance(app_set)
        time_e = statistics.mean(time_set)
        time_v = statistics.variance(time_set)
        
        print("average approximation error: ", app_e)
        print("variance of approximation error: ", app_v)
        print("average time: ", time_e)
        print("variance of time: ", time_v)
    
data = ['../data/polyploid/input_0.txt', '../data/polyploid/input_1.txt', '../data/polyploid/input_2.txt']
main(data)