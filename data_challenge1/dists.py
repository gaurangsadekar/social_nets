import math

def manhattan(coord1, coord2):
    return abs(coord1[1] - coord2[1]) + abs(coord1[0] - coord2[0])

def l2(coord1, coord2):
    return math.sqrt( (coord1[1] - coord2[1]) ** 2 + (coord1[0] - coord2[0]) ** 2 )
