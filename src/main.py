# haplotype phasing for N-ploid organisms
from open_input_file import read_file
from read_range import read_range
from max_coverage import max_coverage
from opt import opt_algo
from build_graph import build_graph
from color_annealing import color_annealing
import numpy as np
import time
import matplotlib.pyplot as plt

def main(path):
    r, s, M, N = read_file(path)
    
    # exact algorithm
    start = time.perf_counter()
    read_range_list = read_range(r, s, M)
    K = max_coverage(read_range_list)
    min_D = opt_algo(r, s, M, read_range_list, K)
    end = time.perf_counter()
    time1 = end -start
    
    # heuristic algorithm
    G = build_graph(r, s, M)
    start = time.perf_counter()
    cost, color, cost_history = color_annealing(r, s, M, N, G)
    end = time.perf_counter()
    time2 = end - start
    
    print("OPT: ", min_D, "Time: ", time1)
    print("ALG: ", cost, "Time: ", time2)
    print("approximation ratio: ", cost / min_D)
    
    # plot
    iteration = []
    for i in range(0, len(cost_history)):
        iteration.append(i)
    plt.plot(iteration, cost_history)
    plt.plot([0, len(cost_history)], [min_D, min_D], color='red')
    plt.xlabel("iteration")
    plt.ylabel("cost")
    plt.show()
    
main('../data/diploid/input_0.txt')