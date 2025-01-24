# heuristic for polyploid phasing: Modeling with graph coloring, then solve with simulated annealing.
from build_graph import build_graph
from bfs_coloring import bfs_coloring
import random
import math
import networkx as nx

def color_annealing(r, s, N, G, H, I, ans, alpha, neighbor_rate):
    cost = 0
    cost_history = []
    T = 0 # initial temperature
    
    # initial coloring
    start = 0 # a vertex which has the maximum degree in G
    for v in G.nodes():
        if G.degree(v) > G.degree(start):
            start = v
    color = bfs_coloring(G, H, start, r, N)
    
    ''' # 初期解としてOPTに近いものを与えてみる
    C = [random.randint(0, r - 1) for _ in range(0)] # 変えるリード
    for c in C:
        color[c] = random.randint(0, N - 1) '''
    
    # initial cost and temperature
    for e in I.edges():
        if color[e[0]] == color[e[1]]:
            cost += I[e[0]][e[1]]['weight']
        T += I[e[0]][e[1]]['weight'] # high temperature
    cost_history.append(cost)
    
    # iteration
    stay = 0
    iteration = 0
    while (T > 0.0001 and stay < 50):
        delta_min = r * s
        delta_min_list = []
        V = [random.randint(0, r - 1) for _ in range(0, round(r * neighbor_rate))]
        for v in V:
            for i in range(0, N):
                if i != color[v]: # change v's color to i
                    delta = 0
                    for u in I.neighbors(v):
                        w = I[v][u]['weight']
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
        
        if delta_min < 0:
            color[v] = i
            cost += delta_min
            stay = 0
        else:
            p = math.exp(-delta_min / T)
            if random.random() < p:
                color[v] = i
                cost += delta_min
                if delta_min > 0:
                    stay = 0
            if delta_min == 0:
                stay += 1
        T *= alpha
        iteration += 1
        cost_history.append(cost)
        
        #if iteration % 100 == 0:
            #print("iteration: ", iteration, "cost: ", cost, "T: ", T)
    
    return cost, color, cost_history