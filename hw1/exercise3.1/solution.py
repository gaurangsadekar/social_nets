import networkx as nx
import sys

# implementing g as a directed graph
g = nx.read_edgelist("./caGrQc.txt", delimiter='\t', create_using=nx.DiGraph(), nodetype=int)

min_degree = sys.maxsize
max_degree = 0

for l in g.adjacency_iter():
    degree = len(l[1])
    min_degree = min(min_degree, degree)
    max_degree = max(max_degree, degree)

print("Max degree:", max_degree)
print("Min degree:", min_degree)

