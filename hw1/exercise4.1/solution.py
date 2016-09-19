import networkx as nx

# I'm implementing the strong tie function only considering
# the edge a -> b and not the edge b -> a as well
# to consider the strong tie A- B as the edge a -> b or the edge b -> a,
# the bi-directional function works
def strong_tie(g, a, b):
    edges_a = g[a]
    if not edges_a.has_key(b):
        return False
    edges_b = g[b]
    for neighbor_a in edges_a.iterkeys():
        if edges_b.has_key(neighbor_a):
            return True
    return False

def strong_tie_bidirectional(g, a, b):
    return strong_tie(g, a, b) and strong_tie(g, b, a)

g = nx.read_edgelist("./caGrQc.txt", delimiter='\t', create_using=nx.DiGraph(), nodetype=int)
g.remove_edges_from(g.selfloop_edges())
print(strong_tie(g, 5233, 10310)) # common neighbor 3466
print(strong_tie_bidirectional(g, 5233, 10310))
