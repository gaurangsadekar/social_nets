from __future__ import print_function
import os
import sys
import networkx as nx
import pickle
import random

class GplusGraph:

    def __init__(self, pickle_file):
        if pickle_file == None:
            path = "./gplus/"
            gplus_files = sorted(os.listdir(path))
            # split into files by type
            gplus_node_files = [gplus_files[i : i + 6] for i in range(0, len(gplus_files), 6)]
            sample_idxs = random.sample(range(0, len(gplus_node_files)), 12)
            sample = [gplus_node_files[i] for i in sample_idxs]

            self.g = nx.DiGraph()
            for egonet in sample:
                node = long(egonet[0].split(".")[0])
                egonet = map(lambda fname: path + fname, egonet)
                print("Processing for node:", node)
                self.process_egonet(node, egonet)
        else:
            with open(pickle_file, "r") as pf:
                self.g = pickle.load(pf)

    def process_egonet(self, node, egonet_names):
        circles, edges, egofeat, feat, featnames, followers = egonet_names
        self.g.add_node(node)
        # add node properties
        self.add_egofeat(node, egofeat)
        # add edges from node to each of the nodes in feat
        self.add_feat(node, feat)
        # add circles for each added edge
        self.add_circles(node, circles)
        # add edges between nodes in this ego net
        self.add_ego_edges(edges)
        self.add_followers(node, followers)

    def add_egofeat(self, node, egofeat):
        with open(egofeat, "r") as ef:
            feats = ef.read()
            self.add_node_props(node, feats.split())

    def add_node_props(self, node, feats):
        genders = [bool(int(f)) for f in feats[:3]]
        gender = None
        if genders == [True, False, False]:
            gender = "M"
        elif genders == [False, True, False]:
            gender = "F"
        elif genders == [False, False, True]:
            gender = "T"
        else:
            gender = "O"
        self.g.node[node]["gender"] = gender

    def add_feat(self, node, feat):
        with open(feat, "r") as featfile:
            for egofeat in featfile.readlines():
                ef = egofeat.split()
                n = long(ef[0])
                self.g.add_edge(node, n)
                print("Currently Processing:", node, n)
                self.add_node_props(n, ef[1:])

    def add_circles(self, node, circlesfile):
        with open(circlesfile, "r") as circle_file:
            cs = circle_file.readlines()
            self.g.node[node]["num_circles"] = len(cs)
            for c in cs:
                csplit = c.split()
                c_name = csplit[0]
                circle_members = [long(n) for n in csplit[1:]]
                circle_str = "circle"
                for cn in circle_members:
                    if circle_str not in self.g[node][cn]:
                        self.g[node][cn][circle_str] = list(c_name)
                    else:
                        self.g[node][cn][circle_str].append(c_name)

    def add_ego_edges(self, edges_file_path):
        temp = nx.read_edgelist(edges_file_path, create_using=nx.DiGraph())
        self.g.add_edges_from(temp.edges())

    def add_followers(self, node, followers_file):
        with open(followers_file, "r") as ff:
            followers = [long(f) for f in ff.readlines()]
            map(lambda f: self.g.add_edge(f, node), followers)

if __name__ == "__main__":
    #pickle_file = "gplus_pickle.p"
    g = GplusGraph(None)
    sample_pickle_file = "gplus_pickle_sample.p"
    #print("Writing pickle file")
    pickle.dump(g, open(sample_pickle_file, "w"))
