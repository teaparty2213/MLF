# heuristic for haplotype phasing by removing odd cycles as many as possible

from open_input_file import read_file
from build_graph import build_graph
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def enumerate_faces(embedding):
    faces = []
    for cycle in embedding.faces_iter():
        faces.append(list(cycle))
    return faces

def main(path):
    r, s, M = read_file(path)
    G = build_graph(r, s, M)
    is_planar, embedding = nx.check_planarity(G, counterexample=False)
    if is_planar:
        print("The graph is planar")
        faces = enumerate_faces(embedding)
        for face in faces:
            print(face)
    else:
        print("The graph is not planar")
    nx.draw(G, with_labels=True)
    plt.show()
    
main('../data/input_1.txt')