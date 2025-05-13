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


def generate_complete_graph(delivery_points):
    graph = {}
    
    for from_point in delivery_points:
        graph[tuple(from_point.pos)] = {}  
        for to_point in delivery_points:
            if from_point.pos != to_point.pos:
                cost = compute_base_cost(from_point.pos, to_point.pos, to_point.weight, to_point.priority)
                graph[tuple(from_point.pos)][tuple(to_point.pos)] = cost
    
    return graph




def generate_oriented_sparse_graph(delivery_points, k=3):

    graph = {}  # Format : {pos1: {pos2: coût}}

    for from_point in delivery_points:
        from_pos = tuple(from_point.pos)
        distances = []

        # tum noktaları arasında mesafe hesaplama
        for to_point in delivery_points:
            to_pos = tuple(to_point.pos)
            if from_pos != to_pos:
                d = euclidean_distance(from_pos, to_pos)
                distances.append((d, to_point))

        # en yakun K komşu tutmak
        distances.sort(key=lambda x: x[0])
        k_nearest = distances[:k]

        graph[from_pos] = {}
        for _, to_point in k_nearest:
            to_pos = tuple(to_point.pos)
            cost = compute_base_cost(from_pos, to_pos, to_point.weight, to_point.priority)
            graph[from_pos][to_pos] = cost

    return graph


def generate_sparse_graph(delivery_points, k=3):
    graph = {}  # Format: {pos1: {pos2: cost}}

    for from_point in delivery_points:
        from_pos = tuple(from_point.pos)
        distances = []

        # diğer tum noktalarindan mesafe hesaplama
        for to_point in delivery_points:
            to_pos = tuple(to_point.pos)
            if from_pos != to_pos:
                d = euclidean_distance(from_pos, to_pos)
                distances.append((d, to_point))

        # Keep the k closest neighbors
        distances.sort(key=lambda x: x[0])
        k_nearest = distances[:k]

        # Add edges for the k nearest neighbors (undirected)
        for _, to_point in k_nearest:
            to_pos = tuple(to_point.pos)
            cost = compute_base_cost(from_pos, to_pos, to_point.weight, to_point.priority)
            
            # Add edge from 'from_pos' to 'to_pos' and vice versa for undirected graph
            if from_pos not in graph:
                graph[from_pos] = {}
            if to_pos not in graph:
                graph[to_pos] = {}

            graph[from_pos][to_pos] = cost
            graph[to_pos][from_pos] = cost  # Reverse the direction for undirected

    return graph


