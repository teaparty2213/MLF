import networkx as nx
import random
from collections import deque

def bfs_coloring(G, H, s, r, N):
    color = [-1] * r
    q = deque()
    q.append(s)
    color[s] = 0
    while (len(q) != 0):
        v = q.popleft()
        for u in G.neighbors(v):
            if color[u] == -1:
                if u in H.neighbors(v): # no mismatch between u and v
                    color[u] = color[v]
                else:
                    color_option = list(range(0, N))
                    for w in G.neighbors(u):
                        if color[w] != -1:
                            color_option[color[w]] = -1
                    color_candidate = []
                    for i in range(0, len(color_option)):
                        if color_option[i] != -1:
                            color_candidate.append(i)
                    if len(color_candidate) > 0:
                        color[u] = random.choice(color_candidate)
                    else:
                        color[u] = random.randint(0, N - 1)
                q.append(u)
    return color