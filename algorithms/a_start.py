import heapq
from datetime import datetime, timedelta
from utils.helpers import euclidean_distance, get_neighbors, is_within_no_fly_zone, has_enough_battery_for_move, apply_penality
from queue import PriorityQueue


grid_width = 100
grid_height = 100

# The grid can be implicit, or you can represent it like this (optional):
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]




def a_star(graph, start, goal, nofly_zones, drone, deliveries):
    start_pos = tuple(start.pos)
    goal_pos = tuple(goal.pos)
    """
    Algorithme A* pour trouver le chemin optimal en tenant compte des zones interdites et des contraintes du drone.
    Utilise un graphe pour récupérer les coûts de déplacement entre les nœuds.
    """
    
    # Fonction heuristique A* (distance à la cible + pénalité de zone interdite)
    def heuristic(n, target, nofly_zones):
        distance_to_target = euclidean_distance(n, target)
        nofly_penalty = apply_penality(n, target, nofly_zones)
        return distance_to_target + nofly_penalty

    def redraw_path(came_from, start_pos, goal_pos):
        path = []
        current_node = goal_pos
        while current_node != start_pos:
            path.append(current_node)
            current_node = came_from.get(current_node)  # Obtenez le nœud précédent
            
            if current_node is None:
                print("Chemin non trouvé !")
                return []  # Si on ne trouve pas de chemin, retour vide

        path.append(start_pos)  # Ajouter le point de départ à la fin
        return path[::-1]  # Retourner le chemin dans l'ordre correct

    # Open set (priorité de la file d'attente)
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start_pos, goal_pos, nofly_zones), 0, start_pos))  # (f, g, n)

    # Dictionnaires pour garder une trace des coûts et des parents
    g_scores = {start_pos: 0}  # Coût depuis le point de départ
    came_from = {}

    while open_set:
        _, current_cost, current_node = heapq.heappop(open_set)

        # Si on arrive au but (livraison)
        if current_node == goal_pos:
            # Utilisation de redraw_path pour obtenir le chemin final
            return redraw_path(came_from, start_pos, goal_pos)

        # Exploration des voisins du graphe
        for neighbor_pos, cost in graph[tuple(current_node)].items():
            neighbor = next((dp for dp in deliveries if tuple(dp.pos) == neighbor_pos), None)
            # Vérification du poids du voisin
            if neighbor.weight <= drone.max_weight:
                battery_needed = euclidean_distance(current_node, neighbor_pos) * 2 / drone.speed  # Aller-retour ##time
                if battery_needed <= drone.battery: #Drone'ların şarj süresini hesaba katın. 

                    penality = apply_penality(current_node, neighbor_pos, nofly_zones)
                    tentative_g_score = current_cost + cost + penality
                    
                    # Si le voisin n'a pas encore été exploré ou si son score est meilleur
                    if tuple(neighbor_pos) not in g_scores or tentative_g_score < g_scores[tuple(neighbor_pos)]:
                        came_from[tuple(neighbor_pos)] = current_node
                        g_scores[tuple(neighbor_pos)] = tentative_g_score
                        #f_score = tentative_g_score + heuristic(neighbor_pos, goal_pos, nofly_zones)
                        f_score = tentative_g_score + euclidean_distance(neighbor_pos, goal_pos)

                        
                        # Si le voisin n'est pas dans open_set ou qu'il a un meilleur score, on l'ajoute
                        #if not any(neighbor_pos == n[2] for n in open_set):
                        heapq.heappush(open_set, (f_score, tentative_g_score, neighbor_pos))
            
        # Debug: vérifier ce qui est ajouté à open_set et came_from
        # print("Open set:", open_set)
        # print("Came from:", came_from)

    return None  # Si aucun chemin trouvé
