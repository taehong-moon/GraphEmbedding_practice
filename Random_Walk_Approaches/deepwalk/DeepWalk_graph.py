""" DeepWalk Algorithm

    Input : graph G(V, E)
            window size ; w
            embedding size ; d
            walks per vertex ; gamma
            walk length ; t

    Output : matrix of vertex representation M

    """

# Errors
""" def degree()
    def number_of_nodes"""
import random
import numpy as np
from collections import defaultdict, Iterable
from itertools import product, permutations, zip_longest

class Graph(defaultdict):

    def __init__(self):

        super(Graph, self).__init__(list)

    def nodes(self):

        return self.keys()

    def adjacency_iter(self): # role?

        return self.items()

    def subgraph(self, nodes=[]):

        subgraph = Graph()

        for sub_node in nodes:
            if sub_node in self:
                subgraph[sub_node] = [x for x in self[sub_node] if x in nodes]

        return subgraph

    def make_undirected(self):

        print('Not Completed')

    def make_consistent(self):

        print('Not Completed')

    def remove_self_loops(self):

        print('Not Completed')

    def check_self_loops(self):

        print('Not Completed')

    # Boolean Function
    def has_edge(self, v1, v2):

        if v2 in self[v1] or v1 in self[v2]: # This code is for both undirected graph and directed graph.
            return True
        return False

    def degree(self, nodes=None): # Must be modified, type : 'int'

        if isinstance(nodes, Iterable):
            return {v:len(self[v]) for v in nodes}
        else:
            return len(self[nodes])

    def number_of_nodes(self):
        """ Returns the number of nodes in the graph"""
        return len(self) # Must be modified # None : [] is added

    def number_of_edges(self):
        """ Retruns the number of edges in the graph"""
        return sum([self.degree(x) for x in self.keys()])/2

    def Random_Walk(self, walk_length, alpha=0, rand=random.Random(), start=None):
        """ Return a truncated  random walk

            walk_length : length of the random walk
            alpha : probability of restart
            start : the start node of the random walk
        """

        G = self
        if start:
            walk = [start]
        else:
            # Sampling is uniformly processed w.r.t Vertices
            walk = [rand.choice(list(G.keys()))]

        while len(walk) < walk_length:
            cur = walk[-1]
            if len(G[cur]) > 0: # Check we can move further from this node
                if rand.random() > alpha: # Probability
                    walk.append(rand.choice(G[cur])) # At the last connected node, we can choose another node
                                                    # Of course, we can go back to previous node
                else:
                    walk.append(walk[0])
            else:
                break

        return [str(node) for node in walk]

    def build_deepwalk_corpus(G, num_walks, walk_length, alpha=0, rand=random.Random()):

        deep_walks = []

        nodes = list(G.nodes())

        for cnt in range(num_walks):
            rand.shuffle(nodes)
            for node in nodes:
                deep_walks.append(G.Random_Walk(walk_length, rand=rand, alpha=alpha, start=node))

        return deep_walks

    def build_deepwalk_corpus_iter(self):

        print('Not Completed')

    def grouper(n, iterable, padvalue=None):
        "grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')"
        return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)

    def load_dataset(file_name):

        graph_data = []

        temp_graphData = open(file_name, 'r', encoding='utf-8')

        for line in temp_graphData:
            temp_str = line.split()
            graph_data.append(temp_str)

        return graph_data

    def given_graph(dataset):

        refined_structure = Graph()

        for adj_node in dataset:
            if adj_node[0] in refined_structure.keys():
                temp_node = list(refined_structure[adj_node[0]])
                temp_node.append(adj_node[-1])
                upgrade_node = temp_node
                refined_structure[adj_node[0]] = upgrade_node
            else:
                refined_structure[adj_node[0]] = adj_node[-1]

        return refined_structure

    def target_community(self):

        print("Not Completed") # How to label the node?



# Test Function!

example_graph = defaultdict(list)
data = [ ['1', ['4', '6', '8', '13']], ['2', ['4', '10', '11', '14', '15']], ['3', ['7']], ['4', ['1', '2', '7', '12']],
        ['5',['7']], ['6', ['1']], ['7', ['3', '4', '5', '9']], ['8', ['1']], ['9', ['7']], ['10', ['2']],
        ['11', ['2']],['12', ['4']], ['13', ['1']], ['14', ['2']], ['15', ['2']] ]


for k, v in data:
    example_graph[k] = v

# print(len(data))
# print(len(example_graph))
#
# print(Graph.subgraph(example_graph, nodes=['1', '2', '4']))
# print(type(Graph.degree(example_graph)))
# print(Graph.number_of_edges(example_graph))
# print(Graph.number_of_nodes(example_graph))
#
# print(Graph.Random_Walk(example_graph, 3))


# r = open('com-youtube.ungraph.txt', 'r', encoding='utf-8')
# temp = []
# while(1):
#     for lines in range(50):
#         temp_str = r.readline().split()
#         temp.append(temp_str)
#     break
#
# print(temp)

test_def1 = Graph.load_dataset('test_file.txt')
print(test_def1)
test_def2 = Graph.given_graph(dataset=test_def1)
print(test_def2)

test_def3 = Graph.load_dataset('com-youtube.all.cmty.txt')
print(test_def3)
print(len(test_def3))

