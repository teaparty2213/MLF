# heuristic to haplotype phasing by removing odd cycles as many as possible

from open_input_file import read_file
from build_graph import build_graph
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

r, s, M = read_file('../data/input_2.txt')
G = build_graph(r, s, M)
# nx.draw(G, with_labels=True)
# plt.show()