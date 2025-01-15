# haplotype phasing for N-ploid organisms
from open_input_file import read_file
from read_range import read_range
from max_coverage import max_coverage
from opt import opt_for_diploid
from build_graph import build_graph
from color_annealing import color_annealing
from open_file_for_polyploid import read_file_of_polyploid
import numpy as np
import time
import matplotlib.pyplot as plt
import networkx as nx

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
    
    N, r, s, M, err_num, ans_list, haplotypes = read_file_of_polyploid(path)
    # heuristic
    start = time.perf_counter()
    G, H = build_graph(r, s, M, read_share_ratio=0.9)
    cost, color, cost_history = color_annealing(r, s, N, G, H, alpha=0.9, neighbor_rate=0.1)
    end = time.perf_counter()
    time2 = end - start
    
    print("N: ", N)
    print("OPT: ", err_num)
    print("ALG: ", cost, "Time: ", time2)
    print("approximation ratio: ", cost / err_num)
    #nx.draw(G)
    #plt.show()
    
    # plot
    iteration = list(range(0, len(cost_history)))
    plt.plot(iteration, cost_history)
    plt.plot([0, len(cost_history)], [err_num, err_num], color='red')
    plt.xlabel("iteration")
    plt.ylabel("cost")
    plt.title("number of errors in {}-ploid".format(N))
    plt.savefig("./../result/250115_{}-ploid.png".format(N))
    plt.show()

#main('../data/diploid/planar_data/input_0.txt')   
main('../data/polyploid/input_1.txt')