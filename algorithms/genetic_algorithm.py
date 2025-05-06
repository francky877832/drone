import random
from math import sqrt

def euclidean_distance(pos1, pos2):
    """Calcule la distance euclidienne entre deux points."""
    x1, y1 = pos1
    x2, y2 = pos2
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate, generations):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations

    def generate_population(self, drones, deliveries):
        """Génère une population initiale de solutions."""
        population = []
        for _ in range(self.population_size):
            solution = {drone: random.choice(deliveries) for drone in drones}
            population.append(solution)
        return population

    def fitness(self, solution):
        """Calcule la 'fitness' d'une solution. Plus c'est bas, mieux c'est."""
        total_cost = 0
        for drone, delivery in solution.items():
            total_cost += euclidean_distance(drone.start_pos, delivery.pos)  # Cost of travel
        return total_cost

    def select_parents(self, population):
        """Sélectionne deux parents en fonction de leur fitness."""
        sorted_population = sorted(population, key=self.fitness)
        return sorted_population[0], sorted_population[1]

    def crossover(self, parent1, parent2):
        """Croisement des parents pour créer un enfant."""
        child = {}
        for drone in parent1:
            child[drone] = parent1[drone] if random.random() > 0.5 else parent2[drone]
        return child

    def mutate(self, solution, deliveries):
        """Mutation d'une solution."""
        for drone in solution:
            if random.random() < self.mutation_rate:
                solution[drone] = random.choice(deliveries)  # Change the delivery for this drone
        return solution

    def evolve(self, population, deliveries):
        """Applique une génération d'algorithme génétique."""
        new_population = []
        for _ in range(self.population_size // 2):
            parent1, parent2 = self.select_parents(population)
            child1 = self.crossover(parent1, parent2)
            child2 = self.crossover(parent2, parent1)
            new_population.append(self.mutate(child1, deliveries))
            new_population.append(self.mutate(child2, deliveries))
        return new_population

    def run(self, drones, deliveries):
        population = self.generate_population(drones, deliveries)
        for generation in range(self.generations):
            population = self.evolve(population, deliveries)
            best_solution = min(population, key=self.fitness)
            print(f"Generation {generation + 1}: Best fitness {self.fitness(best_solution)}")
        return min(population, key=self.fitness)

# Exemple de test
if __name__ == "__main__":
    class Drone:
        def __init__(self, drone_id, start_pos):
            self.drone_id = drone_id
            self.start_pos = start_pos

    class Delivery:
        def __init__(self, delivery_id, pos):
            self.delivery_id = delivery_id
            self.pos = pos

    drones = [Drone(1, (0, 0)), Drone(2, (5, 5))]
    deliveries = [Delivery(1, (2, 2)), Delivery(2, (8, 8))]

    genetic_algo = GeneticAlgorithm(population_size=50, mutation_rate=0.1, generations=100)
    best_solution = genetic_algo.run(drones, deliveries)
    print("Meilleure solution:", best_solution)
