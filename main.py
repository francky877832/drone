
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.data_generator import generate_scenario
from algorithms.a_star import a_star
from algorithms.csp import CSP
from algorithms.genetic_algorithm import GeneticAlgorithm

# Générer les données
drones, deliveries, no_fly_zones = generate_scenario(5, 10, 3)

# Test A* (Pathfinding)
start_pos = (0, 0)
goal_id = 2  # L'ID du point de livraison cible
delivery_graph = {}  # Générer un graph de livraison ici
path, cost = a_star(start_pos, deliveries, delivery_graph, goal_id, no_fly_zones)
print("Path found by A*:", path, "Total cost:", cost)

# Test CSP (Constraint Satisfaction Problem)
csp = CSP(drones, deliveries, no_fly_zones)
valid_assignments = csp.get_valid_assignments()
print("Valid assignments from CSP:", valid_assignments)

# Test Algorithme Génétique
genetic_algo = GeneticAlgorithm(population_size=50, mutation_rate=0.1, generations=100)
best_solution = genetic_algo.run(drones, deliveries)
print("Best solution from Genetic Algorithm:", best_solution)
