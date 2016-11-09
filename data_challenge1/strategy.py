from social_graph import *
import sys
import dists
'''
all node choosing strategies, based on social graph and neighbors
making locally optimal choices at every node
since that will be the case in the testing phase
'''

# returns the neighbor with the highest degree
def highest_degree_neighbor(sg, dest, neighbors, dist_fn=None):
    max_degree = 0
    max_degree_neighbor = None
    for node, info in neighbors:
        deg = info[0]
        if deg > max_degree:
            max_degree = deg
            max_degree_neighbor = node
    return max_degree_neighbor

'''
    for every neighbor, compare the last check in only
    assumes that timestamp ranges are similar
'''
def closest_last_checkin(sg, dest, neighbors, dist_fn=dists.manhattan):
    dest_last_checkin = sg.node_checkins[dest][-1][-1]
    min_dist = sys.maxsize
    closest_neighbor = None
    for node in neighbors.iterkeys():
        if len(sg.node_checkins[node]) > 0:
            node_last_checkin = sg.node_checkins[node][-1][-1]
            dist = dist_fn(node_last_checkin, dest_last_checkin)
            if dist < min_dist:
                min_dist = dist
                closest_neighbor = node
    return closest_neighbor

'''
    for every node, find the check in that is made at the closest time
    as the last ts of the destination
    picks the closest check in to the timestamp for each node,
    and computes the min distance
    unless the timestamps vary remarkably, this should give similar results to the prev function
'''
def closest_time_checkin(sg, dest, neighbors, dist_fn=dists.manhattan):
    dest_last_ts = sg.node_checkins[dest][-1][0]
    dest_last_checkin = sg.node_checkins[dest][-1][-1]
    min_dist = sys.maxsize
    closest_neighbor = None
    for node in neighbors.iterkeys():
        # find the check in for the node at the timestamp
        # closest to the the last checkin of the destination
        checkins = sg.node_checkins[node]
        if len(checkins) > 0:
            closest_ts = None
            closest_checkin = None
            min_diff = sys.maxsize
            for ts, curr_coord in checkins:
                if abs(ts - dest_last_ts) < min_diff:
                    min_diff = abs(ts - dest_last_ts)
                    closest_ts = ts
                    closest_checkin = curr_coord

            dist = dist_fn(closest_checkin, dest_last_checkin)
            if dist < min_dist:
                min_dist = dist
                closest_neighbor = node
    return closest_neighbor

