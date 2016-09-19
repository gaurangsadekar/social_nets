import networkx as nx
import sys

def print_coauthor_metrics(g):
    ca1 = 0
    ca10 = 0
    ca20 = 0
    ca40 = 0
    ca80 = 0
    num_nodes = len(g.nodes())

    for l in g.adjacency_iter():
        num_coauth = len(l[1])
        if num_coauth == 1:
            ca1 += 1
        if num_coauth <= 10:
            ca10 += 1
        if num_coauth <= 20:
            ca20 += 1
        if num_coauth <= 40:
            ca40 += 1
        if num_coauth <= 80:
            ca80 += 1

    print("% of authors with 1 coauthor =", ca1 * 100.0/num_nodes)
    print("% of authors with <= 10 coauthors =", ca10 * 100.0/num_nodes)
    print("% of authors with <= 20 coauthors =", ca20 * 100.0/num_nodes)
    print("% of authors with <= 40 coauthors =", ca40 * 100.0/num_nodes)
    print("% of authors with <= 80 coauthors =", ca80 * 100.0/num_nodes)

g = nx.read_edgelist("./caGrQc.txt", delimiter='\t', create_using=nx.DiGraph(), nodetype=int)
print("Without removing self loops")
print_coauthor_metrics(g)

# there are self loops in the graph
# if we want the same metrics after removing self loops
print("After removing self loops")
g.remove_edges_from(g.selfloop_edges())
print_coauthor_metrics(g)
