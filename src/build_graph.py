import networkx as nx

def read_range(r, s, M):
    range_list = [[0, 0] for i in range(r)]
    for i in range(0, r):
        j = 0
        while M[i][j] == -1:
            j += 1
        range_list[i][0] = j
        while j < s and M[i][j] != -1:
            j += 1
        range_list[i][1] = j - 1
    return range_list 
                
def edge_weight_calc(i, j, M): # compare M[i] and M[j]
    sum = 0
    for k in range(0, len(M[i])):
        if (M[i][k] != '-' and M[j][k] != '-'):
            if (M[i][k] != M[j][k]):
                sum += 1
    return sum
                
def build_graph(r, s, M, read_share_ratio):
    G = nx.Graph() # represents hamming distances between reads
    H = nx.Graph() # connects vertices with an edge if they have no mismatch
    read_range_list = read_range(r, s, M)
    for i in range(0, r):
        G.add_node(i)
        H.add_node(i)
        start_i = read_range_list[i][0]
        end_i = read_range_list[i][1]
        len_i = end_i - start_i + 1
        for j in range(i + 1, r):
            start_j = read_range_list[j][0]
            end_j = read_range_list[j][1]
            shared_len = max(0, end_i - start_j + 1)
            if shared_len >= len_i * read_share_ratio:
                w = edge_weight_calc(i, j, M)
                if w > 0:
                    G.add_edge(i, j, weight=w)
                elif w == 0:
                    H.add_edge(i, j)
    return G, H