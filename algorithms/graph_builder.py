from utils.helpers import compute_cost

def build_graph(start_pos, deliveries):
    graph = {}
    all_points = [("start", start_pos)] + [(d.id, d.pos) for d in deliveries]

    for i, (id1, pos1) in enumerate(all_points):
        graph[id1] = {}
        for j, (id2, pos2) in enumerate(all_points):
            if i != j:
                delivery = next((d for d in deliveries if d.id == id2), None)
                if delivery:
                    cost = compute_cost(pos1, pos2, delivery.weight, delivery.priority)
                else:
                    cost = 0  # start → first node, no delivery yet
                graph[id1][id2] = cost
    return graph
