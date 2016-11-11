import math
from math import radians, cos, sin, asin, sqrt

def manhattan(coord1, coord2):
    return abs(coord1[1] - coord2[1]) + abs(coord1[0] - coord2[0])

def l2(coord1, coord2):
    return sqrt( (coord1[1] - coord2[1]) ** 2 + (coord1[0] - coord2[0]) ** 2 )

# use only for g_fn
# send 2 coords to it, return 1 since there is an edge between the 2
def unweighted(coord1, coord2):
	return 1

# calculate the great circle between 2 points on earth
def haversine(coord1, coord2):
    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # radius of earth in km
    r = 6371
    return c * r

