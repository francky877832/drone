import random
from utils.helpers import euclidean_distance, estimate_arrival_time
from utils.time import is_within_time_window


import random
from utils.helpers import euclidean_distance, estimate_arrival_time, is_within_time_window

def generate_random_individual(drones, deliveries):

    individual = {f"D{d.id}": [] for d in drones}  
    shuffled_deliveries = deliveries.copy() 
    random.shuffle(shuffled_deliveries) 

    for delivery in shuffled_deliveries:
        for drone in drones:
            key = f"D{drone.id}"
            if len(individual[key]) == 0: #constraint , 1 drone = 1 delivery 
                individual[key].append(delivery.id) 
                break 

    return individual



def generate_random_full_individual(drones, deliveries):
    
    individual = {f"D{d.id}": [] for d in drones}  
    shuffled_deliveries = deliveries.copy() 

    assigned = True
    done = True
    while assigned and done :
        random.shuffle(shuffled_deliveries) 
        for delivery in shuffled_deliveries:
            if not assigned :
                assigned = True
                done = False
                break
            for drone in drones:
                if tuple(drone.start_pos) == tuple(delivery.pos) :
                    assigned = False
                    print(f"A drone cannot deliver to his own position. Retrying...{drone.id}:{drone.start_pos} - delivery : {delivery.pos}")
                    break
                key = f"D{drone.id}"
                if len(individual[key]) == 0: #constraint , 1 drone = 1 delivery 
                    individual[key].append(delivery.id) 
                    assigned = True
                    done = True
                    break

    return individual

def generate_initial_population(drones, deliveries, size=5):
    return [generate_random_individual(drones, deliveries) for _ in range(size)]

def generate_initial_full_population(drones, deliveries, size=5):
    return [generate_random_full_individual(drones, deliveries) for _ in range(size)]
