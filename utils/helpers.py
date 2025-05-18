from math import dist
import math
from utils.time import is_within_time_window

import random

fixed_penality = 10

def initialize_drones_on_graph(delivery_points, drones):
    delivery_positions = [tuple(d.pos) for d in delivery_points]
    for drone in drones:
        random_position = random.choice(delivery_positions)
        drone.start_pos = random_position

    return drones


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
            nofly_penalty += fixed_penality  # Pénalité à ajouter si le point est dans la zone interdite
    
    return distance_to_target + nofly_penalty








from datetime import datetime

def is_within_time_window(current_time_str, time_window):
    current_time = datetime.strptime(current_time_str, "%H:%M").time()
    start_time = datetime.strptime(time_window[0], "%H:%M").time()
    end_time = datetime.strptime(time_window[1], "%H:%M").time()
    #print("ok",time_window[0])

    return start_time <= current_time <= end_time


def apply_fixed_penality(start_node, end_node, nofly_zones, drone):
    path = LineString([start_node, end_node]) 
    penality = 0
    for zone in nofly_zones:
        later = get_time_from_noflyzone(drone, zone.polygon)
        #drone can trtaverse a noflyzone when nnot active
        if is_within_time_window(later.strftime("%H:%M"), zone.active_time) :
            if isinstance(zone.polygon, Polygon) and path.intersects(zone.polygon):
                # print("penality", start_node, end_node)
                penality += fixed_penality
    
    return penality




from shapely.geometry import LineString, Polygon, Point
from datetime import datetime, timedelta
from shapely.geometry import Point

def get_time_from_noflyzone(drone, zone):
    start_node = tuple(drone.start_pos)
    now = datetime.strptime(drone.start_time, "%H:%M")
    closest_point = min(zone.exterior.coords, key=lambda coord: Point(coord).distance(Point(start_node)))
    distance = Point(closest_point).distance(Point(start_node)) * 100  # in nmeter

    later = now + timedelta(seconds=distance / drone.speed)

    return later



def apply_penality(start_node, end_node, nofly_zones, drone, cost_per_meter=fixed_penality):
    #print(cost_per_meter)
    path = LineString([start_node, end_node])
    penalty = 0
    penalized_length = 0

    for zone in nofly_zones:
        if not zone.polygon.is_valid:
            # print("Invalid Polygon!")
            zone.polygon = zone.polygon.buffer(0)

        if isinstance(zone.polygon, Polygon) and path.intersects(zone.polygon):
            intersection = path.intersection(zone.polygon)

            # Handle both LineString and MultiLineString results
            if not intersection.is_empty:
                later = get_time_from_noflyzone(drone, zone.polygon)
                # print(later.strftime("%H:%M"))
                # print(zone.active_time)

                #drone can trtaverse a noflyzone when nnot active
                if  is_within_time_window(later.strftime("%H:%M"), zone.active_time) :
                    # print("no nofly_zones violation")
                    if intersection.geom_type == 'LineString':
                        penalized_length = intersection.length
                    elif intersection.geom_type == 'MultiLineString':
                        penalized_length = sum(line.length for line in intersection.geoms)
                    else:
                        penalized_length = 0

                penalty += math.ceil(penalized_length) * cost_per_meter
                # print(f"Penalty applied between {start_node} and {end_node}: {penalized_length:.2f} m")

    return penalty


def compute_cost(start_node, end_node, weight, priority, nofly_zones):
    distance = euclidean_distance(start_node, end_node) 
    base_cost = compute_base_cost(start_node, end_node, weight, priority)
    penalty = 0
    if not is_valid_move(start_node, end_node, nofly_zones):
        penalty = apply_penality(start_node, end_node, nofly_zones, fixed_penality)
    total_cost = base_cost + penalty
    return total_cost








def get_battery_needed(drone, delivery):
    distance_to_delivery = euclidean_distance(drone.current_pos, delivery.pos)
    battery_needed = distance_to_delivery * 2 / drone.speed # roud-trip
    return battery_needed


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

def estimate_arrival_time(start_time_str, distance, speed):

    start_time = datetime.strptime(start_time_str, "%H:%M")

    travel_time_seconds = distance*100 / speed #distance is in cm
    # print(start_time)
    # print(distance)
    
    
    arrival_time = start_time + timedelta(seconds=travel_time_seconds)
    arrival_time = start_time + timedelta(hours=travel_time_seconds)
    
    return arrival_time.strftime("%H:%M")


def compute_average_energy(paths, graph) :
    total_cost = 0
    for idx, path in enumerate(paths):
        path_cost = 0
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            # Use get to avoid KeyError if edge not found
            cost = graph.get(u, {}).get(v)
            if cost is not None:
                path_cost += cost
            else:
                path_cost += 0  
        total_cost += total_cost

    return total_cost/len(path)