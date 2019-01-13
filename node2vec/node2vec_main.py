# Node2vec SKetch
"""
    1. Create a graph
    2. Precompute probabilities and generate walks
    3. Embed nodes
    4. Look for most similar nodes
    5. Save Embeddings for later use
    6. Save model for later use

    cf. Embed edges using Hadamard method
"""

# node2vec.Node2vec parameter
""" 
    Node2vec constructor

    1. graph :  The first positional argument has to be a networkx graph.
                Node names must be all integers or all strings.
                On the output model they will always be strings
    2. dimensions : Embedding dimensions
    3. walk_length : Number of nodes in each walk
    4. num_walks : Number of walks per node
    5. p :  Return hyper parameter
    6. q : Inout parameter
    7. weight_key : On weighted graphs, this it the key for the weight attribute
    8. workers : Number of workers for parallel execution
    9. sampling_strategy : Node specific sampling strategies, supports setting node
                           specific 'q', 'p', 'num_walks' and 'walk_length'
    10. quiet : Boolean controlling the verbosity.(Default : False)
    11. temp_folder : String path pointing to folder to save a shared memory copy of the graph
                      - Supply when working graphs that are too big to fit in memory during
                        algorithm execution.

    Node2vec.fit method : Accepts any key word argument acceptable by gensim.Word2Vec
"""

# node2vec.EdgeEmbedder
"""
    EdgeEmbedder is an abstract class which all the concrete edge embedding class inherit from.
    The classes are {'AverageEmbedder', 'HadamardEmbedder', 'WeightedL1Embedder', 'WeightedL2Embedder'}.
    
    Notice that edge embeddings are defined for any pair of nodes, connected or not even node with itself
    
Constructor
    1. keyed_vectors: A gensim.models.KeyedVectors instance containing the node embeddings
    2. quiet : Boolean controlling the verbosity.(Default : False)

EdgeEmbedder.__getitem__(item) method, better known as 'EdgeEmbedder[item]':
    1. item - A tuple consisting of 2 nodes from the keyed_vectors passed in the constructor.
        Will return the embedding of the edge.
"""

# Confusing function
"""
# dict.get(key, default=None)
    key - This is the Key to be searched in the dictionary
    default - This is the Value to be returned in case key does not exist
# lambda parameter : the way that processing with given parameter
    ex. Make 1**2 , ---, 5**2 
    list(map(lambda x: x**2, (range(1,6))))
# zip, map, and lambda

"""

from collections import defaultdict
import numpy as np
import gensim, os
from joblib import Parallel, delayed
from tqdm import tqdm
from node2vec.node2vec_parallel import parallel_generate_walks

class Node2Vec:

    FIRST_TRAVEL_KEY = 'first_travel_key'
    PROBABILITIES_KEY = 'probabilities'
    NEIGHBORS_KEY = 'neighbors'
    WEIGHT_KEY = 'weight'
    NUM_WALKS_KEY = 'num_walks'
    WALK_LENGTH_KEY = 'walk_length'
    P_KEY = 'p'
    Q_KEY = 'q'

    def __init__(self, graph, dimensions=128, walk_length=80, num_walks=10, p=1, q=1,
                 weight_key='weight', workers=1, sampling_strategy=None, quiet=False, temp_folder=None):

        self.graph = graph
        self.dimensions = dimensions
        self.walk_length = walk_length
        self.num_walks = num_walks
        self.p = p
        self.q = q
        self.weight_key = weight_key
        self.workers = workers
        self.quiet = quiet

        self.d_graph = defaultdict(dict)

        if sampling_strategy is None:
            self.sampling_strategy = {}
        else:
            self.sampling_strategy = sampling_strategy

        # Find another source and understand this part deeply
        self.temp_folder, self.require = None, None
        if temp_folder:
            if not os.path.isdir(temp_folder):
                raise NotADirectoryError("temp_folder does not exist or is not a directory. ({})".format(temp_folder))

            self.temp_folder = temp_folder
            self.require = "sharedmem"

        self._precompute_probabilities()
        self.walks = self._generate_walks()

    # TODO Actually I have no idea of '.nodes()', '.neighbors()', Try to be EXPLICIT!
    def _precompute_probabilities(self):
        """ Precompute transition probabilities for each node. """

        d_graph = self.d_graph
        first_travel_done = set()

        # TODO change this code more intuitively(It's about 'tqdm' package)
        nodes_generator = self.graph.nodes() if self.quiet \
            else  tqdm(self.graph.nodes(), desc='Computing transition probabilities')

        # TODO Make loop and algorithm more simple, considering another options added
        for source in nodes_generator:

            # Init probabilities dict for first travel
            if self.PROBABILITIES_KEY not in d_graph[source]:
                d_graph[source][self.PROBABILITIES_KEY] = dict()

            for current_node in self.graph.neighbors(source):

                # Init probabilities dict
                if self.PROBABILITIES_KEY not in d_graph[current_node]:
                    d_graph[current_node][self.PROBABILITIES_KEY] = dict()

                unnormalized_weights = list()
                first_travel_weights = list()
                d_neighbors = list()

                # Calculate unnormalized weights
                for destination in self.graph.neighbors(current_node):

                    p = self.sampling_strategy[current_node].get(self.P_KEY,
                                                                 self.p) if current_node in self.sampling_strategy else self.p
                    q = self.sampling_strategy[current_node].get(self.Q_KEY,
                                                                 self.q) if current_node in self.sampling_strategy else self.q

                    if destination == source: # Backwards Probability
                        ss_weight = self.graph[current_node][destination].get(self.weight_key, 1) * (1 / p)
                    elif destination in self.graph[current_node]: # If the neighbor is connected to the source
                        ss_weight = self.graph[current_node][destination].get(self.weight_key, 1)
                    else:
                        ss_weight = self.graph[current_node][destination].get(self.weight_key, 1) * (1 / q)

                    # Assign the unnormalized sampling strategy weight, normalize during random walk
                    unnormalized_weights.append(ss_weight)
                    if current_node not in first_travel_done:
                        first_travel_weights.append(self.graph[current_node][destination].get(self.weight_key, 1))
                    d_neighbors.append(destination)

                # Normalize
                unnormalized_weights = np.array(unnormalized_weights)
                d_graph[current_node][self.PROBABILITIES_KEY][source] = unnormalized_weights / unnormalized_weights.sum()

                if current_node not in first_travel_done:
                    unnormalized_weights = np.array(first_travel_weights)
                    d_graph[current_node][self.FIRST_TRAVEL_KEY] = unnormalized_weights / unnormalized_weights.sum()
                    first_travel_done.add(current_node)

                d_graph[current_node][self.NEIGHBORS_KEY] = d_neighbors

    def _generate_walks(self):
        """
            Generates the random walks which will be used as the skip-gram input
            :return: List fo walks. Each walk is a list of nodes.

        """
        flatten = lambda l: [item for sublist in l for item in sublist]

        # Split num_walks for each worker
        num_walks_lists = np.array_split(range(self.num_walks), self.workers)

        walk_results = Parallel(n_jobs=self.workers, temp_folder=self.temp_folder, require=self.require)(
            delayed(parallel_generate_walks)(self.d_graph,
                                             self.walk_length,
                                             len(num_walks),
                                             idx,
                                             self.sampling_strategy,
                                             self.NUM_WALKS_KEY,
                                             self.WALK_LENGTH_KEY,
                                             self.NEIGHBORS_KEY,
                                             self.PROBABILITIES_KEY,
                                             self.FIRST_TRAVEL_KEY,
                                             self.quiet) for idx, num_walks in enumerate(num_walks_lists, 1))

        walks = flatten(walk_results)

        return walks


    def fit(self, **skip_gram_params):
        """
        Creates the embeddings using gensim's Word2Vec.
        :param skip_gram_params: Parameters for gensim.models.Word2Vec - do not supply 'size' it is taken from the Node2Vec 'dimensions' parameter
        :type skip_gram_params: dict
        :return: A gensim word2vec model
        """

        if 'workers' not in skip_gram_params:
            skip_gram_params['workers'] = self.workers

        if 'size' not in skip_gram_params:
            skip_gram_params['size'] = self.dimensions

        return gensim.models.Word2Vec(self.walks, **skip_gram_params)

