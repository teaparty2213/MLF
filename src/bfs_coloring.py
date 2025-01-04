import networkx as nx
import random
from collections import deque

def bfs_coloring(G, s, r, N):
    color = [-1] * r
    q = deque()
    q.append(s)
    color[s] = 0
    while (len(q) != 0):
        v = q.popleft()
        for u in G.neighbors(v):
            if color[u] == -1:
                color_option = list(range(0, N))
                for w in G.neighbors(u):
                    if color[w] != -1:
                        color_option[color[w]] == -1
                for i in range(0, len(color_option)):
                    if color_option[i] != -1:
                        color[u] = color_option[i]
                        break
                if color[u] == -1:
                    color[u] = random.randint(0, N - 1)
                q.append(u)
    return color