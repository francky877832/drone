from math import dist
import math
from utils.time import is_within_time_window


def compute_cost(pos1, pos2, weight, priority):
    distance = dist(pos1, pos2)
    return distance * weight + priority * 100



def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


from datetime import datetime, timedelta


def estimate_arrival_time(drone_start_time, drone_speed_kmh, distance_km):
    # Convertir vitesse en km/h → temps en minutes
    if isinstance(drone_start_time, str):
        drone_start_time = datetime.strptime(drone_start_time, "%H:%M")
    travel_minutes = (distance_km / drone_speed_kmh) * 60
    return drone_start_time + timedelta(minutes=travel_minutes)

