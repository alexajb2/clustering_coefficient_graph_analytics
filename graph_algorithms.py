# explanations for these functions are provided in requirements.py

from graph import Graph
import random
from collections import deque, defaultdict

def BFS(r: int, graph: Graph) -> tuple:
	farthest = -1
	distance = -1
	
	# Using deque as permitted in ED #126
	queue = deque([(r, 0)])
	visited = set([r])
	
	while queue:
		current_node, current_distance = queue.popleft()

		for neighbor in graph.nodes_neighbors[current_node]:
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append((neighbor, current_distance + 1))
				
				# Update the farthest node and its distance
				if current_distance + 1 > distance:
					farthest = neighbor
					distance = current_distance + 1
	return (farthest, distance)


def get_diameter(graph: Graph) -> int:
	# Get list of nodes that have at least one neighbor.
	nodesList = list(graph.nodes_neighbors.keys())
	# If the graph is empty, return 0 as the diameter.
	if not nodesList:
		return 0
	
	D_max = -1
	w = nodesList[random.randint(0, len(nodesList) - 1)]
	distance = 0
	while distance > D_max:
		D_max = distance
		r = w
		farthest, distance = BFS(r, graph)
		w = farthest
	return D_max



def remove_short_paths(graph: Graph) -> deque:
	# this removes start nodes that don't have a path of length 2
	nodes = deque()
	for node, greater_neighbors in graph.nodes_greater_neighbors.items():
		if any(neigh in graph.nodes_greater_neighbors for neigh in greater_neighbors):
			nodes.append(node)
	return nodes

# def get_clustering_coefficient(graph: Graph) -> float:
# 	triangles = 0
# 	nodes = remove_short_paths(graph)

# 	for node in nodes:
# 		for neighbor in graph.nodes_greater_neighbors[node]:
# 			for neighbor2 in graph.nodes_greater_neighbors[neighbor]:
# 				if neighbor2 in graph.nodes_neighbors[node]:
# 					triangles += 1

# 	two_edge_paths = 0
# 	for neighbors in graph.nodes_neighbors.values():
# 		num_neighbors = len(neighbors)
# 		if num_neighbors >= 2:
# 			two_edge_paths += num_neighbors * (num_neighbors - 1) // 2
# 	clustering_coefficient = 3 * triangles / two_edge_paths
# 	return clustering_coefficient

def get_clustering_coefficient(graph: Graph) -> float:
	# First, compute degeneracy ordering.
	# We need to consider all nodes, even isolated ones.
	n = graph.get_num_nodes()
	# Initialize degrees using get_neighbors() so that even nodes not in nodes_neighbors are considered.
	degrees = {u: len(graph.get_neighbors(u)) for u in range(n)}
	max_deg = max(degrees.values(), default=0)
	
	# Buckets: each index holds the set of nodes with that current degree.
	buckets = [set() for _ in range(max_deg + 1)]
	for u, deg in degrees.items():
		buckets[deg].add(u)
	
	ordering = []       # This will be our degeneracy ordering.
	position = {}       # position[u] will store the ordering index of node u.
	
	# We copy degrees to update as we remove vertices.
	current_degrees = degrees.copy()
	
	# Remove nodes iteratively
	for _ in range(n):
		# Find the non-empty bucket with the smallest degree.
		for d, bucket in enumerate(buckets):
			if bucket:
				u = bucket.pop()
				break
		ordering.append(u)
		position[u] = len(ordering) - 1
		
		# "Remove" u: update the degrees of its neighbors that haven't been removed.
		for v in graph.get_neighbors(u):
			# Only consider v if it hasn't been removed (i.e. is in current_degrees)
			if v in current_degrees:
				d_old = current_degrees[v]
				# Remove v from its current bucket.
				buckets[d_old].discard(v)
				# Decrease its degree count.
				current_degrees[v] = d_old - 1
				buckets[d_old - 1].add(v)
		# Mark u as removed.
		current_degrees.pop(u, None)
	
	# Now count triangles using the degeneracy ordering.
	# For each vertex u, let H(u) = {v in N(u) such that position[u] < position[v]}.
	triangles = 0
	for u in range(n):
		# Retrieve neighbors (use set for O(1) membership tests)
		Nu = set(graph.get_neighbors(u))
		# Build the forward neighbors of u
		forward = [v for v in Nu if position[u] < position.get(v, float('inf'))]
		# Check each pair (v, w) in forward neighborhood; if v and w are connected, then u,v,w form a triangle.
		for i in range(len(forward)):
			v = forward[i]
			Nv = set(graph.get_neighbors(v))
			for j in range(i + 1, len(forward)):
				w = forward[j]
				if w in Nv:
					triangles += 1

	# Compute the total number of two-edge paths.
	two_edge_paths = 0
	for u in range(n):
		deg = len(graph.get_neighbors(u))
		if deg >= 2:
			two_edge_paths += deg * (deg - 1) // 2

	if two_edge_paths == 0:
		return 0.0

	clustering_coefficient = 3 * triangles / two_edge_paths
	return clustering_coefficient


def get_degree_distribution(graph: Graph) -> dict[int, int]:
	# returns a dictionary representing the degree distribution of the graph.
	# the keys are the degree, and the values is the number of nodes with that degree
	degree_distribution = {}
	for node in graph.nodes_neighbors:
		degree = len(graph.nodes_neighbors[node])
		if degree in degree_distribution:
			degree_distribution[degree] += 1
		else:
			degree_distribution[degree] = 1
	return degree_distribution