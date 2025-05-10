from utils.helpers import compute_cost, compute_base_cost, euclidean_distance, apply_penality

def build_graph(start_pos, deliveries):
    graph = {}
    all_points = [("start", start_pos)] + [(d.id, d.pos) for d in deliveries]

    for i, (id1, pos1) in enumerate(all_points):
        graph[id1] = {}
        for j, (id2, pos2) in enumerate(all_points):
            if i != j:
                delivery = next((d for d in deliveries if d.id == id2), None)
                if delivery:
                    cost = compute_base_cost(pos1, pos2, delivery.weight, delivery.priority)
                else:
                    cost = 0  # start → first node, no delivery yet
                graph[id1][id2] = cost
    return graph


def generate_graph(delivery_points, no_fly_zones):
    graph = {}  # Dictionnaire pour le graphe (pos1 → {pos2: cost})
    
    for from_point in delivery_points:
        graph[tuple(from_point.pos)] = {}  
        for to_point in delivery_points:
            if from_point.pos != to_point.pos:
                cost = compute_base_cost(from_point.pos, to_point.pos, to_point.weight, to_point.priority)
                graph[tuple(from_point.pos)][tuple(to_point.pos)] = cost
    
    return graph
