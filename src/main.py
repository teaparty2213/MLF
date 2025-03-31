# haplotype phasing for N-ploid organisms
from open_file_for_polyploid import read_file_of_polyploid
from build_graph import build_graph
from color_annealing import color_annealing
from reconstruct_hap import reconstruct_haplotype
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import networkx as nx

def main():
    directory = './data/'
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath) and 'ploid' in filename:
            print(filepath)
            N, r, s, M, err_num, ans_list, haplotypes = read_file_of_polyploid(filepath)
            
            # heuristic
            start = time.perf_counter()
            G, H, I = build_graph(r, s, M, read_share_ratio=0.8)
            cost, color, cost_history = color_annealing(r, s, N, G, H, I, ans_list, alpha=0.9, neighbor_rate=0.1)
            end = time.perf_counter()
            t = end - start
            
            # calculate OPT
            OPT = 0
            for e in I.edges():
                if ans_list[e[0]] == ans_list[e[1]]:
                    OPT += I[e[0]][e[1]]['weight']
            
            # display cost transition
            plt.figure()
            iteration = list(range(0, len(cost_history)))
            plt.plot(iteration, cost_history, label="cost")
            plt.plot([0, len(cost_history)], [OPT, OPT], color='red', label="answer")
            plt.xlabel("iteration")
            plt.ylabel("cost")
            plt.title("number of errors in {}-ploid".format(N))
            plt.legend(loc="upper right")
            plt.savefig("./result/{}-ploid_r={}_s={}_cost.png".format(N, r, s))
            
            # print results
            print("ploidy: {}, number of reads: {}, number of SNP positions: {}".format(N, r, s))
            print("approx ratio: {}".format(cost / OPT))
            print("running time: {}".format(t))
            print("---------------------")
            
            # accuracy evaluation of the prediction 
            reconstruct_haplotype(r, s, N, M, color, haplotypes)
        
main()