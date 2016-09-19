import networkx as nx
import sys

g = nx.read_edgelist("./caGrQc.txt", delimiter='\t', create_using=nx.DiGraph(), nodetype=int)
g.remove_edges_from(g.selfloop_edges())

# using same strong tie function as exercise 4.2
def strong_tie(g, a, b):
    edges_a = g[a]
    if not edges_a.has_key(b):
        return -1 # no edge
    edges_b = g[b]
    for neighbor_a in edges_a.iterkeys():
        if edges_b.has_key(neighbor_a):
            return 1 # strong tie
    return 0 # weak tie

print("No. of connected components in original graph:", nx.number_strongly_connected_components(g))

def len_largest_connected_component(g):
    len_largest = 0
    for component in list(nx.strongly_connected_components(g)):
        len_largest = max(len_largest, len(component))
    print("Length of largest connected component:", len_largest)

len_largest_connected_component(g)
strong_ties = []
weak_ties = []

for edge in g.edges():
    (a, b) = edge
    if strong_tie(g, a, b) == 0:
        weak_ties.append(edge)

g.remove_edges_from(weak_ties)

print("No. of connected components after weak ties removed:", nx.number_strongly_connected_components(g))
len_largest_connected_component(g)
