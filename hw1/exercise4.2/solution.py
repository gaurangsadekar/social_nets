import networkx as nx

# this function checks only in one direction of the edge a -> b
# since we are iterating over all possible edges, it will still
# give the correct answer
def strong_tie(g, a, b):
    edges_a = g[a]
    if not edges_a.has_key(b):
        return -1 # no tie
    edges_b = g[b]
    for neighbor_a in edges_a.iterkeys():
        if edges_b.has_key(neighbor_a):
            return 1 # strong tie
    return 0 # weak tie

g = nx.read_edgelist("./caGrQc.txt", delimiter='\t', create_using=nx.DiGraph(), nodetype=int)
g.remove_edges_from(g.selfloop_edges())

def tie_metrics(g):
    strong_tie_count = 0
    weak_tie_count = 0

    for edge in g.edges():
        (a, b) = edge
        if strong_tie(g, a, b) == 1:
            strong_tie_count += 1
        elif strong_tie(g, a, b) == 0:
            weak_tie_count += 1

    print "# Edges:", len(g.edges())
    print "# Strong Ties in Graph:", strong_tie_count
    print "# Weak Ties in Graph:", weak_tie_count

print("For the directed graph:")
tie_metrics(g)
# making the graph undirected, to check if there is exact symmetry
print("For the undirected graph:")
tie_metrics(g.to_undirected())
