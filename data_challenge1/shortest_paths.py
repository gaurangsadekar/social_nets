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
def astar_distance_based(sg, source, dest, got_neighbors_for, opt, testcase_id=1, g_fn=dists.manhattan, h_fn=dists.manhattan, h_wt=1):
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
                neighbor_h = h_wt * sg.get_dist(neighbor, dest, h_fn)

                if tentative_g < g[neighbor]:
                    g[neighbor] = tentative_g
                    f_score  = g[neighbor] + neighbor_h
                    fq.put((f_score, neighbor))
                    came_from[neighbor] = current

# returns the path in reverse
def reconstructed_path_rev(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path

def get_path(node, neighbor, came_from_source, came_from_dest):
    # process path
    source_path = [p for p in reversed(reconstructed_path_rev(came_from_source, node))]
    dest_path = reconstructed_path_rev(came_from_dest, neighbor)
    path = source_path + dest_path
    return path
    
def expand_frontier(sg, node, start_frontier, target_frontier, 
                    fq, g_source, g_dest, came_from_source, came_from_dest,
                    closed_set, num_queries, 
                    g_fn, h_fn, opt="train"):
    
    if node not in closed_set:
        num_queries.append(1)

    neighbors = sg.get_neighbors(node)
    for neighbor in neighbors:
        if neighbor in target_frontier:
            # path found
            #print("Path found at:", node, neighbor)
            path = get_path(node, neighbor, came_from_source, came_from_dest)
            path_length = g_source[node] + sg.get_dist(node, neighbor, g_fn) + g_dest[neighbor]
            return (path, path_length)
        else:
            # compute h
            neighbor_h = sys.maxsize
            for tn in target_frontier:
                curr_h = g_dest[tn] + sg.get_dist(neighbor, tn, h_fn)
                neighbor_h = min(neighbor_h, curr_h)
            
            # for every neighbor, compute f
            tentative_g = g_source[node] + sg.get_dist(node, neighbor, g_fn)
            if neighbor not in g_source or tentative_g < g_source[neighbor]:
                g_source[neighbor] = tentative_g
                f_score = g_source[neighbor] + neighbor_h
                came_from_source[neighbor] = node
                fq.put((f_score, neighbor))
    # add to start frontier
    for neighbor in neighbors:
        start_frontier.add(neighbor)
    
    return (None, None)

def frontier_search(sg, source, dest, got_neighbors_for, testcase_id=1, g_fn=dists.unweighted, h_fn=dists.manhattan):
    source_frontier = { source }
    closed = set()
    dest_frontier = { dest }
    num_queries = 0
    came_from_source = {}
    came_from_dest = {}
    
    g_source = {}
    g_dest = {}
    for node in sg.node_checkins:
        g_source[node] = sys.maxint
        g_dest[node] = sys.maxint
    g_source[source] = 0
    g_dest[dest] = 0
    
    fq = Queue.PriorityQueue()
    h_source_dest = sg.get_dist(source, dest, h_fn)
    fq.put((h_source_dest, source))
    fq.put((h_source_dest, dest))
    num_queries = []
    while not fq.empty():
        min_f, current = fq.get()
            
        if current in source_frontier:
            res = expand_frontier(sg, current, 
                                  source_frontier, dest_frontier, fq,
                                  g_source, g_dest, 
                                  came_from_source, came_from_dest,
                                  closed, num_queries,
                                  g_fn, h_fn
                                 )
            
        elif current in dest_frontier:
            res = expand_frontier(sg, current, 
                                  dest_frontier, source_frontier, fq,
                                  g_dest, g_source,
                                  came_from_dest, came_from_source,
                                  closed, num_queries,
                                  g_fn, h_fn
                                 )
        closed.add(current)
            
        if res != (None, None):
            path, path_length = res
            if dest == path[0] and source == path[-1]:
                path.reverse()
            return (path, path_length, sum(num_queries))    


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
