from math import dist
import math
from utils.time import is_within_time_window


def compute_base_cost(pos1, pos2, weight, priority):
    distance = dist(pos1, pos2)
    return distance * weight + priority * 100


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def heuristic(n, target, nofly_zones):
    distance_to_target = euclidean_distance(n.pos, target.pos)
    
    nofly_penalty = 0
    for zone in nofly_zones:
        if zone.contains(n.pos) or zone.contains(target.pos):
            nofly_penalty += 1000  # Pénalité à ajouter si le point est dans la zone interdite
    
    return distance_to_target + nofly_penalty



def compute_cost(start_node, end_node, weight, priority, nofly_zones):
    distance = euclidean_distance(start_node, end_node) 
    base_cost = compute_base_cost(start_node, end_node, weight, priority)
    penalty = 0
    if not is_valid_move(start_node, end_node, nofly_zones):
        penalty = 1000  # Pénalité si le chemin traverse une zone interdite
    total_cost = base_cost + penalty
    return total_cost


def get_neighbors(current_node, graph):
    neighbors = []
    for neighbor, cost in graph.get(current_node, []):
        print(f"Neighbor: {neighbor}, Cost: {cost}")
        neighbors.append(neighbor)
    return neighbors


def is_valid_move(start_node, end_node, nofly_zones):
    """Vérifie si un mouvement entre start_node et end_node est valide (ne traverse pas une zone interdite)."""
    path = [start_node, end_node]
    
    for zone in nofly_zones:
        for point in path:
            if zone.contains(point): 
                return False
    
    return True


from shapely.geometry import LineString, Polygon

def apply_penality(start_node, end_node, nofly_zones):
    """Vérifie si un mouvement entre start_node et end_node traverse une zone interdite."""
    path = LineString([start_node, end_node]) 
    penality = 0
    for zone in nofly_zones:

        if isinstance(zone.polygon, Polygon) and path.intersects(zone.polygon):
            # print("penality", start_node, end_node)
            penality += 10000
    
    return penality










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

