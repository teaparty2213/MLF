# heuristic for polyploid phasing: Modeling with graph coloring, then solve with simulated annealing.
from build_graph import build_graph
from bfs_coloring import bfs_coloring
import random
import math
import networkx as nx

def color_annealing(r, s, M, N, G, H):
    cost = 0
    cost_history = []
    T = 0 # initial temperature
    
    # initial coloring
    start = 0 # a vertex which has the maximum degree in G
    for v in G.nodes():
        if G.degree(v) > G.degree(start):
            start = v
    color = bfs_coloring(G, H, start, r, N)
    for e in G.edges():
        if color[e[0]] == color[e[1]]:
            cost += G[e[0]][e[1]]['weight']
        T += G[e[0]][e[1]]['weight'] # high temperature
    T /= r
    cost_history.append(cost)
    
    # iteration
    stay = 0
    while (stay < 20 and T > 0.0001):
        delta_min = r * s
        delta_min_list = []
        for v in range(0, r):
            for i in range(0, N):
                if i != color[v]: # change v's color to i
                    delta = 0
                    for u in G.neighbors(v):
                        w = G[v][u]['weight']
                        if color[u] == i:
                            delta += w
                        elif color[u] == color[v]:
                            delta -= w
                    if delta < delta_min:
                        delta_min_list = []
                        delta_min = delta
                        delta_min_list.append((v, i))
                    elif delta == delta_min:
                        delta_min_list.append((v, i))
        v, i = random.choice(delta_min_list)
        
        if delta_min <= 0:
            color[v] = i
            cost += delta_min
            if delta_min == 0:
                stay += 1
        else:
            p = math.exp(-delta_min / T)
            if random.random() < p:
                color[v] = i
                cost += delta_min
                stay = 0
            else:
                stay += 1
        T *= 0.95
        cost_history.append(cost)
    
    return cost, color, cost_history