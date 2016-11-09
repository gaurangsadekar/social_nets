from __future__ import print_function
from social_graph import SocialGraph
from neighbor_server import *
import sys
import strategy

'''
    get the shortest path between source and destination
    making locally optimal decisions
'''
def get_shortest_path_for_testcase(sg, source, dest, testcase_id, got_neighbors_for, strategy=None):
    reached_dest = False
    path = []
    api_counter = 0

    curr_source = source
    while not reached_dest:
        print("Current Source is:", curr_source)
        path.append(curr_source)

        # check if limit is reached before querying server
        if api_counter >= 150:
            print("Too many requests for the test case, returning path so far")
            break
        # get neighbors from server
        neighbors = None
        if curr_source not in got_neighbors_for:
            print("Getting neighbors for:", curr_source)
            neighbors = get_neighbors(curr_source, testcase_id)
            got_neighbors_for.add(curr_source)
            api_counter += 1
        # get neighbors from graph itself, since we have already asked for neighbors
        else:
            neighbors = sg.get_neighbors(curr_source)

        #neighbor_nodes = set([tup[0] for tup in neighbors])
        if dest in neighbors:
            path.append(dest)
            print("Destination found")
            reached_dest = True
        else:
            # add neighbors into the graph
            sg.add_all_neighbor_data(curr_source, neighbors)
            # pick a neighbor to go to, based on strategy
            best_neighbor_to_follow = strategy(sg, dest, neighbors)
            print("Jumping to:", best_neighbor_to_follow)
            curr_source = best_neighbor_to_follow

    return (path, api_counter, got_neighbors_for)

def get_shortest_paths(sg, testcase_id, source, dest):
    optimization_fn = strategy.closest_last_checkin
    got_neighbors_for = set()
    shortest_path, api_counter, got_neighbors_for = get_shortest_path_for_testcase(sg, source, dest, testcase_id, got_neighbors_for, optimization_fn)
    print("Shortest Path:", shortest_path)
    print("API Requested:", api_counter)
    print("Got neighbors from API for:", got_neighbors_for)
    return shortest_path

def main():
    opt = sys.argv[1]
    sg = SocialGraph(opt)

    if opt == "train":
        # get testcase from system.in
        more_input = True
        while more_input:
            testcase_id = 1
            source = raw_input("Enter Source:")
            dest = raw_input("Enter Destination:")

            source = int(source)
            dest = int(dest)

            shortest_path = get_shortest_paths(sg, testcase_id, source, dest)
            more_input_str = raw_input("More Input? :")
            more_input = True if more_input_str == "y" or more_input_str == "Y" else False

    elif opt == "test":
        # get the testcases from the server
        for testcase_id in range(1, 2):
            source, dest = get_testcase(testcase_id)
            shortest_path = get_shortest_paths(sg, testcase_id, source, dest)
            results = {}
            results[testcase_id] = shortest_path

            # submit to the server
            print("Not submitting anything right now")
            #for t_id, path in results.iteritems():
            #    submit_path_for_testcase(testcase_id, shortest_path)

if __name__ == "__main__":
    main()
