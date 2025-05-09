import json
from models.drone import Drone
from models.delivery import Delivery
from models.no_fly_zone import NoFlyZone
from algorithms.graph_builder import build_graph
from ga.population import generate_initial_population, generate_initial_smart_population
from utils.constraints import check_constraints, check_constraints_with_penality



with open("scenario1.json", "r") as f:
    data = json.load(f)

drones = [Drone(**d) for d in data["drones"]]
deliveries = [Delivery(**d) for d in data["deliveries"]]
no_fly_zones = [NoFlyZone(**z) for z in data["no_fly_zones"]]

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

for i, ind in enumerate(population):
    print(f"\nIndividu {i+1} :")
    for drone, tasks in ind.items():
        print(f"  {drone} -> {tasks}")

    is_valid, violations = check_constraints(ind, drones, deliveries, no_fly_zones)
    print(is_valid)
    if is_valid:
        print("Contrainst uygundur.")
    else:
        pass
        print("Contrainsts ihmaldir :")
        for v in violations:
            print(f"   - {v}")

#constrainst with penality
"""for i, ind in enumerate(population):
    print(f"\nIndividu {i+1} :")
    for drone, tasks in ind.items():
        print(f"  {drone} → {tasks}")

    penalty, violations = check_constraints_with_penality(ind, drones, deliveries, no_fly_zones)
    print("Valide :", penalty == 0)
    if violations:
        print("Kısıt ihlalleri:")
        for v in violations:
            print(" ", v)
    else:
        print("Tüm kısıtlar geçildi.")"""


from ga.fitness import compute_fitness 

for i, individu in enumerate(population):
    fitness, violations = compute_fitness(individu, drones, deliveries, no_fly_zones)
    print(f"\nIndividu {i+1} : Fitness = {fitness:.2f}, Violations = {len(violations)}")
    if violations:
        for v in violations:
            print(f" {v}")

