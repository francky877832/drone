from math import dist
import math


def compute_cost(pos1, pos2, weight, priority):
    distance = dist(pos1, pos2)
    return distance * weight + priority * 100



def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
