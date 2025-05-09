import random
def crossover(parent1, parent2):
    # Yeni çocuk bireyi oluştur
    child = {}

    for drone_id in parent1:
        # Her bir drone için ya parent1 ya da parent2'den görevleri seç
        if random.random() < 0.5:
            child[drone_id] = parent1[drone_id][:]
        else:
            child[drone_id] = parent2[drone_id][:]

    return child


def mutate(individual):
    drone_ids = list(individual.keys())

    if len(drone_ids) < 2:
        return individual  # Mutation impossible

    drone1, drone2 = random.sample(drone_ids, 2)

    if individual[drone1] and individual[drone2]:
        d1 = random.choice(individual[drone1])
        d2 = random.choice(individual[drone2])

        # Contrôle avant suppression
        if d1 in individual[drone1] and d2 in individual[drone2]:
            individual[drone1].remove(d1)
            individual[drone2].remove(d2)

            individual[drone1].append(d2)
            individual[drone2].append(d1)

    return individual



