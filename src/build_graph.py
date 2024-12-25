import networkx as nx

def edge_weight_calc(i, j, M): # compare M[i] and M[j]
    sum = 0
    for k in range(0, len(M[i])):
        if (M[i][k] != '-' and M[j][k] != '-'):
            if (M[i][k] != M[j][k]):
                sum += 1
    return sum
                
def build_graph(r, s, M):
    G = nx.Graph()
    for i in range(0, r):
        for j in range(i + 1, r):
            w = edge_weight_calc(i, j, M)
            if w > 0:
                G.add_edge(i, j, weight=w)
    return G