from __future__ import print_function
from social_graph import SocialGraph
from neighbor_server import *
import sys
import Queue
import dists
'''
get the shortest path between source and destination
making locally optimal decisions
'''
#def get_shortest_path_for_testcase(sg, source, dest, testcase_id, got_neighbors_for, strategy=None):
#    reached_dest = False
#    path = []
#    api_counter = 0
#
#    curr_source = source
#    while not reached_dest:
#        print("Current Source is:", curr_source)
#        path.append(curr_source)
#
#        # check if limit is reached before querying server
#        if api_counter >= 150:
#            print("Too many requests for the test case, returning path so far")
#            break
#        # get neighbors from server
#        neighbors = None
#        if curr_source not in got_neighbors_for:
#            print("Getting neighbors for:", curr_source)
#            neighbors = get_neighbors(curr_source, testcase_id)
#            got_neighbors_for.add(curr_source)
#            api_counter += 1
#        # get neighbors from graph itself, since we have already asked for neighbors
#        else:
#            neighbors = sg.get_neighbors(curr_source)
#
#        #neighbor_nodes = set([tup[0] for tup in neighbors])
#        if dest in neighbors:
#            path.append(dest)
#            print("Destination found")
#            reached_dest = True
#        else:
#            # add neighbors into the graph
#            sg.add_all_neighbor_data(curr_source, neighbors)
#            # pick a neighbor to go to, based on strategy
#            best_neighbor_to_follow = strategy(sg, dest, neighbors)
#            print("Jumping to:", best_neighbor_to_follow)
#            curr_source = best_neighbor_to_follow
#
#    return (path, api_counter, got_neighbors_for)

#def get_shortest_paths(sg, testcase_id, source, dest):
#    optimization_fn = strategy.closest_last_checkin
#    got_neighbors_for = set()
#    shortest_path, api_counter, got_neighbors_for = get_shortest_path_for_testcase(sg, source, dest, testcase_id, got_neighbors_for, optimization_fn)
#    print("Shortest Path:", shortest_path)
#    print("API Requested:", api_counter)
#    print("Got neighbors from API for:", got_neighbors_for)
#    return shortest_path

'''
	calculate shortest paths using A* like strategy using hueristics
    cost is calculate using g_fn and hueristic is defined by h_fn
    pass distance metric to the call

    1. for task 1, using unweighted edges and manhattan/l2 hueristic should work (testing pending)
    2. for task 2, using manhattan distance or some combination should work (testing pending)

    returns path, path length (no. of edges or geographic movement) and neighbors for whom API is queried for
'''
def astar_distance_based(sg, source, dest, got_neighbors_for, opt, testcase_id=1, g_fn=dists.manhattan, h_fn=dists.manhattan):
    closed_set = set()
    # used to reconstruct path after finding destination
    num_queries = 0
    came_from = {}
    g = {}
    for node in sg.node_checkins:
        g[node] = sys.maxsize
    g[source] = 0
    fq = Queue.PriorityQueue()

    # initialize heap with start node
    fq.put((sg.get_dist(source, dest, h_fn), source))
    while not fq.empty():
        min_f, current = fq.get()

        if current == dest:
            print("Destination Reached")
            print("Number of Queries made:", num_queries)
            return (reconstructed_path(came_from, current), g[current], num_queries, got_neighbors_for)
        
        if current in closed_set:
            continue

        closed_set.add(current)

        neighbors = None
        if opt == "train":
            neighbors = sg.get_neighbors(current)
            num_queries += 1
        elif opt == "test":
            if current not in got_neighbors_for:
                print("Getting neighbors for:", current)
                neighbors = get_neighbors(current, testcase_id, opt)
                num_queries += 1
                got_neighbors_for.add(current)
            else:
                neighbors = sg.get_neighbors(current)

        for neighbor in neighbors.iterkeys():
            if neighbor not in closed_set:
                tentative_g = g[current] + sg.get_dist(current, neighbor, g_fn)
                neighbor_h = sg.get_dist(neighbor, dest, h_fn)

                if tentative_g < g[neighbor]:
                    g[neighbor] = tentative_g
                    f_score  = g[neighbor] + neighbor_h
                    fq.put((f_score, neighbor))
                    came_from[neighbor] = current

def reconstructed_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return [p for p in reversed(path)]

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

            shortest_path, path_length, got_neighbors_for = astar_distance_based(
                sg, source, dest, got_neighbors_for, opt, testcase_id, g_fn=dists.unweighted, h_fn=dists.manhattan
            )
            more_input_str = raw_input("More Input? :")
            more_input = True if more_input_str == "y" or more_input_str == "Y" else False

    elif opt == "test":
        # get the testcases from the server
        # testcases for task 1
        results = {}
        got_neighbors_for = set()
        for testcase_id in range(1, 21):
            source, dest = get_testcase(testcase_id, opt)
            shortest_path, path_length, got_neighbors_for = astar_distance_based(
                sg, source, dest, got_neighbors_for, opt, testcase_id, g_fn=dists.unweighted, h_fn=dists.manhattan
            )
            results[testcase_id] = (shortest_path, path_length)

        for testcase_id in range(21, 41):
            source, dest = get_testcase(testcase_id, opt)
            shortest_path, geog_length, got_neighbors_for = astar_distance_based(
                sg, source, dest, got_neighbors_for, opt, testcase_id, g_fn=dists.manhattan, h_fn=dists.manhattan
            )
            results[testcase_id] = (shortest_path, geog_length)

            # submit to the server
            print("Not submitting anything right now")
            pickle.dump(results, open("test_results.p", "w"))
            #for t_id, path in results.iteritems():
            #    submit_path_for_testcase(testcase_id, shortest_path)

def submit_testcases(results):
    results_list = sorted(results.items(), key = lambda tup: tup[0])
    for t_id, v in results_list:
        shortest_path, path_length = v
        submit_path_for_testcase(t_id, shortest_path)


if __name__ == "__main__":
    main()
