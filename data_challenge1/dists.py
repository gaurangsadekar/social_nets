import math

def manhattan(coord1, coord2):
    return abs(coord1[1] - coord2[1]) + abs(coord1[0] - coord2[0])

def l2(coord1, coord2):
    return math.sqrt( (coord1[1] - coord2[1]) ** 2 + (coord1[0] - coord2[0]) ** 2 )

# use only for g_fn
# send 2 coords to it, return 1 since there is an edge between the 2
def unweighted(coord1, coord2):
	return 1

# no hueristic, use only for h_fn
def no_dist(coord1, coord2):
    return 0
