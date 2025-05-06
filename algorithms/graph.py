from math import sqrt

def euclidean_distance(pos1, pos2):
    """Calcule la distance euclidienne entre deux points."""
    x1, y1 = pos1
    x2, y2 = pos2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def build_delivery_graph(deliveries):
    """Construit un graph des distances entre les points de livraison."""
    graph = {}
    for delivery in deliveries:
        graph[delivery.id] = {}
        for other in deliveries:
            if delivery.id != other.id:
                graph[delivery.id][other.id] = euclidean_distance(delivery.pos, other.pos)
    return graph

# Exemple de test
if __name__ == "__main__":
    class Delivery:
        def __init__(self, delivery_id, pos):
            self.delivery_id = delivery_id
            self.pos = pos

    deliveries = [Delivery(1, (0, 0)), Delivery(2, (3, 4)), Delivery(3, (6, 8))]
    graph = build_delivery_graph(deliveries)
    print("Delivery Graph:", graph)
