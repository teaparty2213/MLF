import networkx as nx

def read_len(r, s, M):
    read_len_list = [0] * r
    for i in range(0, r):
        for j in range(0, s):
            if M[i][j] != '-':
                read_len_list[i] += 1
    return read_len_list 
                
def edge_weight_calc(i, j, M): # compare M[i] and M[j]
    sum = 0
    shared_len = 0
    for k in range(0, len(M[i])):
        if (M[i][k] != '-' and M[j][k] != '-'):
            shared_len += 1
            if (M[i][k] != M[j][k]):
                sum += 1
    return sum, shared_len
                
def build_graph(r, s, M):
    G = nx.Graph() # represents hamming distances between reads
    H = nx.Graph() # connects vertices with an edge if they have no mismatch
    read_len_list = read_len(r, s, M)
    for i in range(0, r):
        G.add_node(i)
        H.add_node(i)
        for j in range(i + 1, r):
            w, shared_len = edge_weight_calc(i, j, M)
            if w > 0:
                G.add_edge(i, j, weight=w)
            elif w == 0 and shared_len > (read_len_list[i] + read_len_list[j]) / 2 * 0.3:
                H.add_edge(i, j)
    return G, H