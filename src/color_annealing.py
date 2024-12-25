# heuristic for polyploid phasing: Modeling with graph coloring, then solve with simulated annealing and beam search.
from build_graph import build_graph
import random

def color_annealing(r, s, M, N, G):
    cost = 0
    # initial coloring
    color = [-1] * r
    for i in range(r):
        color[i] = random.randint(0, N - 1)
    for e in G.edges():
        if color[e[0]] == color[e[1]]:
            cost += 1
            
    # iteration
    
    return cost, color