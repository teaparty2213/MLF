import networkx as nx
import random
from collections import deque

def bfs_coloring(G, H, start, r, s, N):
    color = [-1 for _ in range(r)]
    q = deque()
    q.append(start) # enqueue start vertex (maximum degree in G)
    color[start] = 0
    
    while (len(q) != 0):
        v = q.popleft()
        for u in G.neighbors(v):
            if color[u] == -1: # if u is not colored
                if u in H.neighbors(v): # no mismatch between u and v
                    color[u] = color[v]
                else: # choose a best color for u
                    color_option = list(range(0, N))
                    min_cost = s # maximum value of cost change, same as INF
                    min_color = -1
                    
                    for w in G.neighbors(u):
                        if color[w] != -1:
                            color_option[color[w]] = -1 # color[w] is not available
                            min_cost = min(min_cost, G[u][w]['weight'])
                            if min_cost == G[u][w]['weight']:
                                min_color = color[w]
                                
                    color_candidate = [] # available colors for u
                    for i in range(0, len(color_option)):
                        if color_option[i] != -1:
                            color_candidate.append(i)
                            
                    if len(color_candidate) > 0:
                        color[u] = random.choice(color_candidate) # if there are available colors, randomly select one
                    else:
                        color[u] = min_color # if all colors are already used in neighbors, select the minimum cost color
                q.append(u)
    return color