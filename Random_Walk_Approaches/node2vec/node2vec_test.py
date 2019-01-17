# import networkx as nx
#
# temp = nx.read_gml('lesmiserables.gml')
# print(temp.nodes())
# print(temp.edges())

import gensim
from collections import defaultdict




class Node2Vec:

    """
        According to Node2Vec paper...
        Input : Graph(V, E), Dimensions d, Walk_per_node r, Walk_length l, Context_size k, hyper-parameter (p, q)
        Output : mapping function f(matrix form)

        Python Implementation...
        <class Node2Vec>
        Input : Graph(V, E), Dimensions d, Walk_per_node r, Walk_length l, hyper-parameter (p, q)
        Output : Walk(list)

        <class Node2Vec.fit()>
        Input : ... , **skip_gram_params
        Output : mapping function f(matrix form)


    """
    FIRST_TRAVEL_KEY = 'first_travel_key'
    PROBABILITIES_KEY = 'probabilities'
    NEIGHBORS_KEY = 'neighbors'
    WEIGHT_KEY = 'weight'
    NUM_WALKS_KEY = 'num_walks'
    WALK_LENGTH_KEY = 'walk_length'
    P_KEY = 'p'
    Q_KEY = 'q'

    def __init__(self, graph, dimensions=128, walk_length=80, walk_per_node=10, p=1, q=1,
                 workers=1, sampling_strategy=None):

        self.graph = graph
        self.dimensions = dimensions
        self.walk_length = walk_length
        self.walk_per_node = walk_per_node
        self.p = p
        self.q = q
        self.workers = workers

        if sampling_strategy is None:
            self.sampling_strategy = {}
        else:
            self.sampling_strategy = sampling_strategy

        self.d_graph = defaultdict(dict)
        self._move_probabilities()
        self.walks = self._generate_walks()

        pass

    def _move_probabilities(self):

        d_graph = self.d_graph
        first_travel_done = set()

        node_generator = d_graph.nodes()

        for source in node_generator:

            if self.PROBABILITIES_KEY not in d_graph[source]:
                d_graph[source][self.PROBABILITIES_KEY] = dict()

            for current_node in self.graph.neighbors(source):

                if self.PROBABILITIES_KEY not in d_graph[current_node]:
                    d_graph[current_node][self.PROBABILITIES_KEY] = dict()

                unnormalized_weights = list()
                first_travel_weights = list()
                d_neighbors = list()

                for destination in self.graph.neighbors(current_node):

                    if destination == source: # Backwards Probability
                        ss_weight = self.graph[current_node][destination].get(self.weight_key, 1) * (1 / self.p)
                    elif destination in self.graph[current_node]: # If the neighbor is connected to the source
                        ss_weight = self.graph[current_node][destination].get(self.weight_key, 1)
                    else:
                        ss_weight = self.graph[current_node][destination].get(self.weight_key, 1) * (1 / self.q)

                    # Assign the unnormalized sampling strategy weight, normalize during random walk
                    unnormalized_weights.append(ss_weight)
                    if current_node not in first_travel_done:
                        first_travel_weights.append(self.graph[current_node][destination].get(self.weight_key, 1))
                    d_neighbors.append(destination)





        # Init probabilities dict for first travel

        # Calculate unnormalized weights
        # Assign the unnormalized sampling strategy weight, normalize during random walk
        # Normalize

        pass

    def _generate_walks(self):

        pass

    def fit(self, **skip_gram_params):

        if 'workers' not in skip_gram_params:
            skip_gram_params['workers'] = self.workers

        if 'size' not in skip_gram_params:
            skip_gram_params['size'] = self.dimensions

        return gensim.models.Word2Vec(self.walks, **skip_gram_params)


