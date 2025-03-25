
# Clustering Coefficient Algorithm
The clustering coefficient is a measure used in network analysis to describe how tightly knit a node's neighborhood is. It essentially tells you the degree to which nodes in a graph tend to cluster together. To calculate the Clustering Coefficient, we can calculate the ratio of three times the number of triangles in the graph to the number of connected triples. Below is an explanation of how the algorithm .

## Graph Algorithm Functions and Uses
From interconnected highways to social media networks—graphs can represent many real-world systems. The issue is that observing such systems is no simple matter. In [graph_algorithms.py](graph_algorithms.py), you will find simple methods to calcualte the degree distribution, number of edges, and number of nodes. Alongside this is a sophisticated heuristic for getting the diameter of the graph. Lastly, is the O(d^2 * n) Clustering Coefficient algorithm which counts the number of triangles further explained below. Whether you are tackling traffic congestion, managing complex relations, or fitting any problem that can be represented by a graph—these graph algorithms can be used for analytics and visualization. Below is an example of such a graph.

[Simple Graph Example](Graph_from_Algorithm_Tests.png)

## Clustering Coefficient Algorithm: Counting Triangles

### most naive way O(n^3)
loop through every node three times and count each triangle that exists

### Best way: O("degeracy"^2 * n)
A graph is said to be 𝑘-degenerate if every subgraph of that graph has at least one vertex with degree ≤k.

for u in all nodes:     O(n)
    for v in nodes adjacent to u:   O(# nodes adjacent to u), O(max degree) O(n)
        for w in nodes adjacent to u: (or adjacent to v) O(# nodes adjacent to u)
            if v adjacent to w: (or u adjacent to w)
                add to count

Notes:
- to avoid triple Counting, only check u, v, w where u < v < w.
- Degeneracy pop nodes in sorted order biggest to smallest (bucket).