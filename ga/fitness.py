import random
from datetime import datetime, timedelta
from utils.helpers import euclidean_distance, estimate_arrival_time
from utils.time import is_within_time_window
from utils.constraints import check_all_csp, check_all_csp_for_violation
from algorithms.a_start import a_star

from datetime import datetime, timedelta




def evaluate_individual(individual, graph, no_fly_zones, drones, deliveries):
    total_energy = 0
    total_violations = 0
    successful_deliveries = 0

    for drone_id, delivery_sequence in individual.items():

        drone = next(d for d in drones if f"D{d.id}" == drone_id)
        drone.reset() 

        for delivery_id in delivery_sequence:
            delivery = next(d for d in deliveries if d.id == delivery_id) 
            needed_cost = 0
            path = []

            try:
                start = next(d for d in deliveries if tuple(d.pos) == tuple(drone.start_pos))
                goal = next(d for d in deliveries if tuple(d.pos) == tuple(delivery.pos))
            except StopIteration:
                total_violations += 1
                continue

            path = a_star(graph, start, goal, no_fly_zones, drone, deliveries)
            if not path:
                total_violations += 1
                continue

            for i in range(len(path)-1):
                needed_cost += graph[path[i]][path[i+1]]

            total_violations += check_all_csp_for_violation(start, goal, drone, delivery, needed_cost)

            # Simuler la livraison
            drone.current_weight = delivery.weight
            drone.move(delivery.pos)
            drone.update_battery(needed_cost)
            delivery.complete()

            drone.start_recharge(1000)

            estimated_arrival_time = estimate_arrival_time(
                drone.start_time,
                euclidean_distance(start.pos, goal.pos),
                drone.speed
            )

            try:
                arrival_time = datetime.strptime(estimated_arrival_time, "%H:%M")
            except:
                total_violations += 1
                continue

            time_to_charge = timedelta(minutes=drone.recharge_time)
            time_to_deliver = timedelta(minutes=drone.current_weight * 0.1)

            drone.start_time = (arrival_time + time_to_charge + time_to_deliver).strftime("%H:%M")

            drone.current_weight = 0
            drone.decrement_recharge_time()
            drone.is_recharging = False

            total_energy += needed_cost
            successful_deliveries += 1

    fitness = (successful_deliveries * 50) - (total_energy * 0.1) - (total_violations * 1000)
    return fitness
