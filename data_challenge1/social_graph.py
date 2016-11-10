from __future__ import print_function
import requests
import networkx as nx
import pickle
import os
import csv

class SocialGraph:

    # pass either 'train' or 'test' as opt
    def __init__(self, opt):
        self.init_checkins(opt)
        self.init_network(opt)
        # remove self loops after initializing
        self.network.remove_edges_from(self.network.selfloop_edges())

    def init_network(self, opt):
        print("Initializing network")
        if opt == "train":
            self.network = nx.read_edgelist("usersGPS_larg_comp_training.txt", nodetype=int, create_using=nx.Graph())
        elif opt == "test":
            network = nx.Graph()
            network.add_nodes_from(self.node_checkins.iterkeys())
            self.network = network

    # initialize the checkins from the file
    # global util function that initializes the checkins class variable
    def init_checkins(self, opt):
        print("Initializing check ins")
        if opt == "test":
            checkin_pickle_file = "checkins.p"

            if checkin_pickle_file in os.listdir("."):
                print("Loading from Pickle File")
                node_checkins = pickle.load(open(checkin_pickle_file, "r"))
            else:
                # parse the csv file
                node_checkins = {}
                csv_reader = csv.reader(open("checkin_usersGPS_largcomp_index.csv", "r"))
                for check_in in csv_reader:
                    node = int(float(check_in[0]))
                    if node not in node_checkins:
                        node_checkins[node] = []
                    check_in_tuple = (long(float(check_in[-1])),
                                      tuple(map(lambda x: float(x), check_in[1:-1])))
                    node_checkins[node].append(check_in_tuple)
                # sort all checkins by timestamp
                node_checkins = dict([(node, sorted(checkins, key = lambda tup: tup[0]))
                                      for node, checkins in node_checkins.iteritems()])
                # cache parsed data into a pickle file
                pickle.dump(node_checkins, open(checkin_pickle_file, "w"))

        elif opt == "train":
            checkin_pickle_file = "checkins_train.p"
            if checkin_pickle_file in os.listdir("."):
                print("Loading from Training Pickle File")
                node_checkins = pickle.load(open(checkin_pickle_file, "r"))
            else:
                node_checkins = {}
                csv_reader = csv.reader(open("checkin_usersGPS_largcomp_training.csv", "r"))
                for check_in in csv_reader:
                    node = int(float(check_in[0]))
                    check_in_tuple = (long(float(check_in[-1])),
                                      tuple(map(lambda x: float(x), check_in[1:-1])))
                    if (node not in node_checkins) or node_checkins[node][0][0] < check_in_tuple[0]:
                        node_checkins[node] = [check_in_tuple]
                pickle.dump(node_checkins, open(checkin_pickle_file, "w"))
        self.node_checkins = node_checkins

    '''
    add edges to the network as data is received from the server,
    put degree and local clustering coefficient with edge as well
    aids to build the test graph as each test case can add to the same state
    keys are deg and local_clu
    '''
    def set_neighbor_degree_and_cluster_coeff(self, source, dest, degree=0, clu=0.0):
        self.network.add_edge(source, dest, deg=degree, local_clu=clu)

    def add_all_neighbor_data(self, source, neighbors):
        for n, info in neighbors.iteritems():
            deg = info["deg"]
            clu = info["local_clu"]
            self.set_neighbor_degree_and_cluster_coeff(source, n, deg, clu)
        self.network.remove_edges_from(self.network.selfloop_edges())

    def get_neighbors(self, source):
        return self.network[source]

    def get_location(self, node):
        return self.node_checkins[node][-1][1]

    # calculate coordinate distance
    def get_dist(self, source, dest, dist_fn):
        return dist_fn(self.get_location(source), self.get_location(dest))

