import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_generator import generate_scenario
from algorithms.a_star import a_star

def test_route_planning():
    # Générer des données d'exemple
    drones, deliveries, no_fly_zones = generate_scenario(5, 10, 2)

    # Créer une instance de l'algorithme A*
    AStart = a_star(drones, deliveries, no_fly_zones)

    # Planifier les routes
    routes = AStart.plan_routes()

    # Afficher les résultats
    for route in routes:
        print(f"Drone {route['drone_id']} will deliver to delivery {route['delivery_id']}")

# Lancer le test
test_route_planning()
