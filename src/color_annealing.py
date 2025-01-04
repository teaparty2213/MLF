# heuristic for polyploid phasing: Modeling with graph coloring, then solve with simulated annealing.
from build_graph import build_graph
from bfs_coloring import bfs_coloring
import random
import math
import networkx as nx

def update_C(G, color, C, v):
    for u in G.neighbors(v): # check if all neighbors of neighbor(v) have different colors
        all_dif = True
        for w in G.neighbors(u):
            if color[w] == color[u]:
                all_dif = False
                break
        if all_dif:
            C[u] = 0
        else:
            C[u] = 1
    all_dif = True # check if all neighbors of v have different colors
    for u in G.neighbors(v):
        if color[u] == color[v]:
            all_dif = False
            break
    if all_dif:
        C[v] = 0
    else:
        C[v] = 1
    return C

def color_annealing(r, s, M, N, G):
    cost = 0
    cost_history = []
    T = 0 # initial temperature
    C = [0] * r # 1 = vertices that have the same color with their neighbors
    
    # initial coloring
    start = 0 # a vertex which has the maximum degree in G
    for v in G.nodes():
        if G.degree(v) > G.degree(start):
            start = v
    color = bfs_coloring(G, start, r, N)
    for e in G.edges():
        if color[e[0]] == color[e[1]]:
            cost += G[e[0]][e[1]]['weight']
        T += G[e[0]][e[1]]['weight']
    T /= r
    for v in G.nodes():
        for u in G.neighbors(v):
            if color[v] == color[u]:
                C[v] = 1
                break
    cost_history.append(cost)
    
    # iteration
    stay = 0
    while (stay < 20 and T > 0.0001):
        delta_min = r * s
        best_v = -1
        new_color = -1
        for v in range(0, r):
            for i in range(0, N):
                if i != color[v]:
                    delta = 0
                    for u in G.neighbors(v):
                        if color[u] == i:
                            delta += G[v][u]['weight']
                        if color[u] == color[v]:
                            delta -= G[v][u]['weight']
                    if delta < delta_min:
                        delta_min = delta
                        best_v = v
                        new_color = i
        delta = delta_min
        v = best_v
        i = new_color
        
        if delta <= 0:
            color[v] = i
            cost += delta
            C = update_C(G, color, C, v)
            if delta == 0:
                stay += 1
        else:
            p = math.exp(-delta / T)
            if random.random() < p:
                color[v] = i
                cost += delta
                C = update_C(G, color, C, v)
                stay = 0
            else:
                stay += 1
        T *= 0.95
        cost_history.append(cost)
    
    return cost, color, cost_history