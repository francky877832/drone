from math import dist
import math
from utils.time import is_within_time_window


def compute_cost(pos1, pos2, weight, priority):
    distance = dist(pos1, pos2)
    return distance * weight + priority * 100



def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def is_within_no_fly_zone(nx, ny, no_fly_zones):
    for zone in no_fly_zones :
        if zone.contains((nx, ny)):
            return True
    return False

def has_capacity_for_delivery(drone, delivery):
    return delivery.weight <= drone.max_weight


def used_energy(distance, weight) :
    return distance * weight
#energy_used = dist * energy_per_km * (delivery.weight / drone.max_weight)


def has_enough_battery_for_move(drone, nx, ny):
    distance = euclidean_distance(drone.current_pos, (nx, ny))
    
    energy_needed = used_energy(distance, drone.max_weight)  # You can use drone.weight if it's available
    
    return drone.battery >= energy_needed



from datetime import datetime, timedelta


def estimate_arrival_time(drone_start_time, drone_speed_kmh, distance_km):
    # Convertir vitesse en km/h → temps en minutes
    if isinstance(drone_start_time, str):
        drone_start_time = datetime.strptime(drone_start_time, "%H:%M")
    travel_minutes = (distance_km / drone_speed_kmh) * 60
    return drone_start_time + timedelta(minutes=travel_minutes)

