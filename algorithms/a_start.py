import heapq
from datetime import datetime, timedelta
from utils.helpers import euclidean_distance, is_within_no_fly_zone, has_enough_battery_for_move
from queue import PriorityQueue


grid_width = 100
grid_height = 100

# The grid can be implicit, or you can represent it like this (optional):
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

class State:
    def __init__(self, position, time, energy_consumed, drone, parent=None):
        self.position = position
        self.time = time
        self.energy_consumed = energy_consumed
        self.drone = drone
        self.parent = parent

def get_cost(current_pos, next_pos, drone, delivery):
    # Calculate the Euclidean distance between current and next positions
    dist = euclidean_distance(current_pos, next_pos)
    # Energy consumed (distance * weight of the drone)
    energy_cost = dist * delivery.weight
    # Time (distance / speed)
    time_cost = dist / drone.speed
    return energy_cost, time_cost

def heuristic(current_pos, goal_pos, no_fly_zones):
    # Calculate the Euclidean distance to the goal
    dist = euclidean_distance(current_pos, goal_pos)
    penalty = 0
    
    # Add no-fly zone penalty
    for zone in no_fly_zones:
        if zone.contains(current_pos):
            penalty += 100  # Apply a penalty for no-fly zones
    
    return dist + penalty


import heapq

def astar(start_pos, goal_pos, drone, no_fly_zones, delivery):
    start_pos = tuple(start_pos)
    open_list = PriorityQueue()
    open_list.put((0, start_pos))  # Start node with initial cost of 0
    came_from = {}
    print(start_pos)
    g_score = {start_pos: 0}
    f_score = {start_pos: heuristic(start_pos, goal_pos, no_fly_zones)}  # f(n) = g(n) + h(n)
    
    closed_list = set()  # This will store visited nodes as tuples (hashable)
    
    while not open_list.empty():
        _, current_pos = open_list.get()

        if current_pos == goal_pos:
            return reconstruct_path(came_from, current_pos)
        
        closed_list.add(tuple(current_pos))  # Convert current_pos to a tuple before adding
        
        for neighbor in get_neighbors(current_pos, drone, no_fly_zones):
            if tuple(neighbor) in closed_list:  # Check if neighbor has already been visited
                continue

            energy_cost, time_cost = get_cost(current_pos, neighbor, drone, delivery)
            tentative_g_score = g_score[current_pos] + energy_cost

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_pos
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal_pos, no_fly_zones)
                open_list.put((f_score[neighbor], neighbor))

    return None  # If no path is found



def reconstruct_path(parent_map, end_state):
    path = []
    current_state = end_state
    while current_state in parent_map:
        path.append(current_state)
        current_state = parent_map[current_state]
    path.reverse()
    return path


def get_neighbors(current_pos, drone, no_fly_zones):
    # Assuming the drone moves in 4 directions (up, down, left, right)
    neighbors = []
    
    # Get current x, y position
    x, y = current_pos
    
    # List of potential movements (4 directions)
    potential_neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

    # For each potential neighbor, check if it's valid
    for nx, ny in potential_neighbors:
        if is_valid_position(nx, ny, drone, no_fly_zones):
            neighbors.append((nx, ny))
    
    return neighbors


def is_valid_position(nx, ny, drone, no_fly_zones):
    # nx = delivery.pos[0]
    # ny = delivery.pos[1]
    # 1. Check if the position is within the grid bounds
    if not (0 <= nx < grid_width and 0 <= ny < grid_height):
        return False

    # 2. Check if the position is within any no-fly zone
    if is_within_no_fly_zone(nx, ny, no_fly_zones):
        return False

    # 3. Check if the drone can physically reach the position (e.g., within energy and weight limits)
    if not has_enough_battery_for_move(drone, nx, ny):
        return False
    


    # Additional checks (optional) can be added here, for example:
    # - Collision avoidance (if other obstacles exist)
    # - Checking for wind conditions, etc.
    
    return True
