import heapq
from algorithms.graph import euclidean_distance
from utils.geometry import crosses_no_fly_zone

NO_FLY_PENALTY = 1_000_000  # Large penalty to discourage flying through no-fly zones

def heuristic(current_pos, goal_pos):
    return euclidean_distance(current_pos, goal_pos)

def a_star(start_pos, deliveries, delivery_graph, goal_id, no_fly_zones=[]):
    """
    A* pathfinding from a start position to a delivery point, avoiding no-fly zones.
    """
    delivery_map = {d.id: d for d in deliveries}
    goal = delivery_map[goal_id]

    # Create a pseudo-node for the start position
    start_id = -1
    delivery_map[start_id] = type("Start", (), {"pos": start_pos})
    delivery_graph[start_id] = {
        d.id: euclidean_distance(start_pos, d.pos) for d in deliveries
    }

    # Priority queue: (f_cost, node_id, path, g_cost)
    open_set = []
    heapq.heappush(open_set, (0, start_id, [start_id], 0))
    visited = set()

    while open_set:
        f_cost, current_id, path, g_cost = heapq.heappop(open_set)

        if current_id == goal_id:
            return path, g_cost

        if current_id in visited:
            continue
        visited.add(current_id)

        current_pos = delivery_map[current_id].pos

        for neighbor_id, base_cost in delivery_graph.get(current_id, {}).items():
            if neighbor_id in visited:
                continue

            neighbor_pos = delivery_map[neighbor_id].pos
            cost = base_cost

            if crosses_no_fly_zone(current_pos, neighbor_pos, no_fly_zones):
                cost += NO_FLY_PENALTY

            new_g = g_cost + cost
            h = heuristic(neighbor_pos, goal.pos)
            new_f = new_g + h

            heapq.heappush(open_set, (new_f, neighbor_id, path + [neighbor_id], new_g))

    return None, float('inf')  # No path found
