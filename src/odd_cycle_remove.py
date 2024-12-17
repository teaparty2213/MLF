# heuristic for haplotype phasing by removing odd cycles

from open_input_file import read_file
from build_graph import build_graph
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

def find_odd_cycles(G):
    cycles = nx.chordless_cycles(G) # chord: an edge that is not part of the cycle but connects two nodes in the cycle
    odd_cycles = [cycle for cycle in cycles if len(cycle) % 2 == 1]
    return odd_cycles

def odd_cycle_remove(G, s):
    non_bipartite = True
    sum = 0
    while (non_bipartite):
        odd_cycles = find_odd_cycles(G)
        if len(odd_cycles) == 0:
            non_bipartite = False
        else:
            cycle_edges = []
            for cycle in odd_cycles:
                edges = [(cycle[i], cycle[i + 1]) if i + 1 < len(cycle) else (cycle[i], cycle[0]) for i in range(len(cycle))]
                for edge in edges:
                    weight = G[edge[0]][edge[1]]['weight']
                    cycle_edges.append((edge, weight))
            min_weight = min(cycle_edges, key=lambda x: x[1])[1]
            min_edges = [edge for edge, weight in cycle_edges if weight == min_weight]
            selected_edge = random.choice(min_edges)
            sum += selected_edge[1]
            G.remove_edge(*selected_edge)
    return sum

def main(path):
    r, s, M = read_file(path)
    G = build_graph(r, s, M)
    is_planar, embedding = nx.check_planarity(G, counterexample=False)
    sum = odd_cycle_remove(G, s)
    print(sum)
    
main('../data/input_1.txt')