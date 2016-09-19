import networkx as nx
import sys

g = nx.read_edgelist("./caGrQc.txt", delimiter='\t', create_using=nx.DiGraph(), nodetype=int)
g.remove_edges_from(g.selfloop_edges())

print("Directed edges:", len(g.edges()))
print("Undirected edges:", len(g.edges()))

# this function checks only in one direction of the edge a -> b
def strong_tie(g, a, b):
    edges_a = g[a]
    if not edges_a.has_key(b):
        return -1
    edges_b = g[b]
    for neighbor_a in edges_a.iterkeys():
        if edges_b.has_key(neighbor_a):
            return 1
    return 0

strong_tie_count = 0
weak_tie_count = 0

for edge in g.edges():
    (a, b) = edge
    if strong_tie(g, a, b) == 1:
        strong_tie_count += 1
    elif strong_tie(g, a, b) == 0:
        weak_tie_count += 1

print("# Strong Ties:", strong_tie_count)
print("# Weak Ties:", weak_tie_count)
