
# explanations for member functions are provided in requirements.py
# each file that uses a graph should import it from this file.

from collections.abc import Iterable
from collections import defaultdict

class Graph:
	def __init__(self, num_nodes: int, edges: Iterable[tuple[int, int]]):
		self.num_nodes = num_nodes
		self.edges = list(edges)
		self.num_edges = 0

		nodes_greater_neighbors = defaultdict(list)
		for edge in self.edges:
			node1, node2 = min(edge[0], edge[1]), max(edge[0], edge[1])
			if node1 in nodes_greater_neighbors:
				nodes_greater_neighbors[node1].add(node2)
			else:
				nodes_greater_neighbors[node1] = {node2}
		self.nodes_greater_neighbors = nodes_greater_neighbors

		# using defaultdict as permitted in ED #126
		self.nodes_neighbors = defaultdict(list)
		for node1, node2 in self.edges:
			self.num_edges += 1
			if node1 in self.nodes_neighbors:
				self.nodes_neighbors[node1].add(node2)
			else:
				self.nodes_neighbors[node1] = {node2}
			if node2 in self.nodes_neighbors:
				self.nodes_neighbors[node2].add(node1)
			else:
				self.nodes_neighbors[node2] = {node1}
		self.nodes_neighbors = self.nodes_neighbors
		
	def get_num_nodes(self) -> int:
		return self.num_nodes

	def get_num_edges(self) -> int:
		return self.num_edges

	def get_neighbors(self, node: int) -> Iterable[int]:
		return list(self.nodes_neighbors.get(node, []))