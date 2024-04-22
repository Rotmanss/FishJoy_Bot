import random

import networkx as nx
import matplotlib.pyplot as plt


def generate_complete_graph(num_nodes, weight):
    G = nx.complete_graph(num_nodes)

    for u, v in G.edges:
        G.edge[u, v]['weight'] = random.randint(1, 100)

    return G


