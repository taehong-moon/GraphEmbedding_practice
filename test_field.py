"""
    NetworkX's Data Structure

    NetworkX uses a “dictionary of dictionaries of dictionaries” as the basic network data structure.
    The keys are nodes so G[u] returns an adjacency dictionary keyed by neighbor to the edge attribute dictionary.
    G[u][v] returns the edge attribute dictionary itself

    @ Advantages of dict-of-dicts-of-dicts data structure:

        - Find edges and remove edges with two dictionary look-ups.
        - Prefer to “lists” because of fast lookup with sparse storage.
        - Prefer to “sets” since data can be attached to edge.
        - G[u][v] returns the edge attribute dictionary.
        - 'n in G' tests if node n is in graph G.
        - 'for n in G:' iterates through the graph.
        - 'for nbr in G[n]:' iterates through neighbors.
"""

import networkx as nx
from node2vec.node2vec_main import Node2Vec

# Create a graph
graph = nx.fast_gnp_random_graph(n=100, p=0.5)

# Precompute probabilities and generate walks - **ON WINDOWS ONLY WORKS WITH workers=1**
node2vec = Node2Vec(graph, dimensions=64, walk_length=30, num_walks=200, workers=4)  # Use temp_folder for big graphs

# Embed nodes
model = node2vec.fit(window=10, min_count=1, batch_words=4)