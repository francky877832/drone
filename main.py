import json
import random
from models.drone import Drone
from models.delivery import Delivery
from models.no_fly_zone import NoFlyZone
from algorithms.graph_builder import build_graph
from ga.population import generate_initial_population, generate_initial_smart_population
from utils.constraints import check_constraints, check_constraints_with_penality
from ga.ga import crossover, mutate
from ga.fitness import compute_fitness 
from algorithms.a_start import astar



with open("scenario1.json", "r") as f:
    data = json.load(f)

drones = [Drone(**d) for d in data["drones"]]
deliveries = [Delivery(**d) for d in data["deliveries"]]
no_fly_zones = [NoFlyZone(**z) for z in data["no_fly_zones"]]
population_size = len(drones)

# print(drones[0].max_weight)

graph = build_graph(drones[0].start_pos, deliveries)

#print("Graphe généré :", graph)

print("\nGénération de la population initiale...")
population = generate_initial_population(drones, deliveries, size=5)
population = generate_initial_smart_population(drones, deliveries, size=5)

def check_empty_population(population):
    for idx, individu in enumerate(population):
        if all(len(livraisons) == 0 for livraisons in individu.values()):
            print(f"Birey {idx + 1}: Hiçbir drone'a teslimat atanmamış. Yebi bir senaryo seciniz.")





def run_genetic_algorithm(drones, deliveries, no_fly_zones, generations=20, population_size=5):
    # Başlangıç popülasyonunu oluştur
    population = generate_initial_smart_population(drones, deliveries, population_size)
    check_empty_population(population)
    for gen in range(generations):
        print(f"\n{gen + 1}. Nesil:")

        fitness_scores = []
        for i, individual in enumerate(population):
            score, violations = compute_fitness(individual, drones, deliveries, no_fly_zones)
            fitness_scores.append((individual, score))
            print(f"Birey {i+1} : Fitness = {score:.2f}, İhlaller = {len(violations)}")

        # En iyi bireyleri sırala (fitness'e göre azalan)
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        best_individuals = [fs[0] for fs in fitness_scores[:2]]  # elitizm: en iyi 2 birey korunur


        # Yeni nesil için liste hazırla
        new_population = best_individuals[:]

        # Yeni bireyler üret
        while len(new_population) < population_size:
            parent1 = random.choice(best_individuals)
            parent2 = random.choice(best_individuals)
            child = crossover(parent1, parent2)
            mutated_child = mutate(child)
            new_population.append(mutated_child)

        population = new_population

    # En iyi bireyi döndür
    best_ind, best_score = max(fitness_scores, key=lambda x: x[1])
    print(f"\nEn iyi birey bulundu. Fitness = {best_score:.2f}")
    return best_ind

print("Gelişim başlatılıyor...")
best_solution = run_genetic_algorithm(drones, deliveries, no_fly_zones)
print(best_solution)



grid_width = 100
grid_height = 100

# The grid can be implicit, or you can represent it like this (optional):
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

for individual in population:
        for drone_id, deliveries_for_drone in individual.items():
            drone = next(d for d in drones if d.id == int(drone_id[1:]))  # Find the drone object
            
            for delivery_id in deliveries_for_drone:
                delivery = next(d for d in deliveries if d.id == delivery_id)  # Find the delivery object
                
                # Apply A* to get the optimal path for this drone to this delivery
                start_pos = drone.current_pos
                goal_pos = delivery.pos
                optimal_path = astar(start_pos, goal_pos, drone, no_fly_zones, delivery)
                
                # Update drone's route and other relevant data
                if optimal_path:
                    print(f"Drone {drone.id} has an optimal route to delivery {delivery.id}: {optimal_path}")
                    drone.current_pos = goal_pos  # Update drone position after delivery
                else:
                    print(f"No optimal path found for Drone {drone.id} to Delivery {delivery.id}")


