
from typing import Collection
import requirements

from collections.abc import Iterable

# Instructions
# Some test cases for the Graph class and the graph algorithms can be found in the main block below.
#
# Note that passing the test cases here does not necessarily mean that your graph class or graph
# algorithms are correctly implemented / will pass other cases. It is a good idea to try and create
# different test cases for both.

def create_and_verify_graph(num_nodes: int, edges: Collection[tuple[int, int]]) -> requirements.Graph:
	print(f'\nTesting graph = ({num_nodes}, {edges})')
	graph = requirements.Graph(num_nodes, edges)
	print(f'get_num_nodes(): {graph.get_num_nodes()}, Expected: {num_nodes}')
	print(f'get_num_edges(): {graph.get_num_edges()}, Expected: {len(edges)}')

	return graph

def verify_neighbors(graph: requirements.Graph, node: int, neighbors: 'Iterable[int]'):
	print(f'get_neighbors({node}): {sorted(graph.get_neighbors(node))}, Expected: {sorted(neighbors)}')

def graph_tests():
	print('testing Graph class')

	graph = create_and_verify_graph(0, {})

	graph = create_and_verify_graph(1, {})

	graph = create_and_verify_graph(2, {})
	verify_neighbors(graph, 0, {})
	verify_neighbors(graph, 1, {})

	graph = create_and_verify_graph(2, {(0, 1)})
	verify_neighbors(graph, 0, {1})
	verify_neighbors(graph, 1, {0})

	graph = create_and_verify_graph(3, {})
	verify_neighbors(graph, 0, {})
	verify_neighbors(graph, 1, {})
	verify_neighbors(graph, 2, {})

	graph = create_and_verify_graph(3, {(0, 1), (1, 2)})
	verify_neighbors(graph, 0, {1})
	verify_neighbors(graph, 1, {0, 2})
	verify_neighbors(graph, 2, {1})

	graph = create_and_verify_graph(3, {(0, 1), (1, 2), (0, 2)})
	verify_neighbors(graph, 0, {1, 2})
	verify_neighbors(graph, 1, {0, 2})
	verify_neighbors(graph, 2, {0, 1})

def graph_algorithm_tests():
	print('\ntesting graph algorithms\n')

	graph = requirements.Graph(10, {(0, 3), (0, 7), (1, 4), (1, 5), (1, 6), (2, 3), (2, 7), (3, 4), (3, 8), (3, 9), (4, 5), (4, 9), (5, 6), (8, 9)})
	print(f'get_diameter(): {requirements.get_diameter(graph)}, Expected: 5')
	print(f'get_clustering_coefficient(): {requirements.get_clustering_coefficient(graph)}, Expected: 0.4')
	print(f'get_degree_distribution(): {requirements.get_degree_distribution(graph)}, Expected: { {2: 5, 3: 3, 4: 1, 5: 1} }')

if __name__ == '__main__':
	graph_tests()
	graph_algorithm_tests()