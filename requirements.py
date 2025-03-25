
# Import each one of your sorting algorithms below as follows:
# Feel free to comment out these lines before your algorithms are implemented.
from graph import Graph # type: ignore
from graph_algorithms import get_diameter # type: ignore
from graph_algorithms import get_clustering_coefficient # type: ignore
from graph_algorithms import get_degree_distribution # type: ignore

# Details about Gradescope submission:

# - The graph class should be stored in separate files from the three graph algorithms.
# - No file should include anything outside of standard Python libraries.
# - Functions should be tested using Python 3.6+ on a Linux environment.
# - The submission should either be the files themselves, or a zip file not containing any directories.


# Explanations for Graph public member functions
#
# init(): initialize the graph a given number of nodes and given edges.
#         edges are represented as tuples (u, v), where each edge is between node with index u and
#         node with index v.
#         the autograder will never add duplicate edges to the graph.
# get_num_nodes(): returns the number of nodes in the graph.
# get_num_edges(): returns the number of edges in the graph.
# get_neighbors(): given a node index, return an iterable type over the collection of its neighbors.
#                  the iterable type can be a list, set, generator, etc.
#                  each neighbor should appear exactly once.

# Explanations for graph algorithm functions
#
# get_diameter(): return the approximate graph diameter using a heuristic function.
# get_clustering_coefficient(): return the graph's global clustering coefficient.
# get_degree_distribution(): returns a dictionary representing the degree distribution of the graph.
#                            the keys are the degree, and the values is the number of nodes with that
#                            degree.