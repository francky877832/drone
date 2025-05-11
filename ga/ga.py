import random
from ga.fitness import evaluate_individual

import random

def crossover(parent1, parent2):
    # Convert parents' dictionary values to lists of deliveries
    parent1_deliveries = [parent1[key] for key in parent1]
    parent2_deliveries = [parent2[key] for key in parent2]

    # Choose a crossover point
    crossover_point = random.randint(1, len(parent1_deliveries) - 1)

    # Swap the deliveries after the crossover point
    offspring1_deliveries = parent1_deliveries[:crossover_point] + parent2_deliveries[crossover_point:]
    offspring2_deliveries = parent2_deliveries[:crossover_point] + parent1_deliveries[crossover_point:]

    # Rebuild the offspring dictionaries
    offspring1 = {key: offspring1_deliveries[i] for i, key in enumerate(parent1)}
    offspring2 = {key: offspring2_deliveries[i] for i, key in enumerate(parent2)}

    return offspring1, offspring2


def mutate(individual, deliveries):
    # Randomly select a drone and delivery to mutate
    drone_key = random.choice(list(individual.keys()))
    drone_deliveries = individual[drone_key]

    if not drone_deliveries:
        return 

    delivery_to_remove = random.choice(drone_deliveries)
    
    if delivery_to_remove in drone_deliveries:
        drone_deliveries.remove(delivery_to_remove)

    available_delivery = random.choice([d.id for d in deliveries if d.id != delivery_to_remove]) 
    drone_deliveries.append(available_delivery)

    individual[drone_key] = drone_deliveries





def tournament_selection(population,  graph, no_fly_zones, drones, deliveries, tournament_size=3):
    tournament = random.sample(population, tournament_size)
    tournament.sort(key=lambda individual: evaluate_individual(individual, graph, no_fly_zones, drones, deliveries), reverse=True)
    return tournament[0]  # Best individual



def generate_next_generation(population, graph, no_fly_zones, drones, deliveries, mutation_probability=0.1):
    new_population = []
    
    # Keep the best individual (elitism) if you want
    new_population.append(tournament_selection(population,  graph, no_fly_zones, drones, deliveries))
    
    # Generate new individuals through crossover
    while len(new_population) < len(population):
        parent1 = tournament_selection(population,  graph, no_fly_zones, drones, deliveries)
        parent2 = tournament_selection(population,  graph, no_fly_zones, drones, deliveries)
        
        offspring1, offspring2 = crossover(parent1, parent2)
        
        # Apply mutation with a certain probability
        if random.random() < mutation_probability:
            mutate(offspring1, deliveries)
        
        if random.random() < mutation_probability:
            mutate(offspring2, deliveries)
        
        new_population.append(offspring1)
        new_population.append(offspring2)
    
    return new_population
