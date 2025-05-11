import heapq
from time import sleep
from utils.helpers import get_battery_needed
from algorithms.a_start import a_star

def simulate(graph, drones, deliveries, no_fly_zones, delivery_heap):
    # Simulation - on itère tant qu'il y a des livraisons
    tick_count = 0
    max_ticks = 100  # Limite de temps pour éviter une boucle infinie
    while delivery_heap and tick_count < max_ticks:
        print(f"Tick: {tick_count}")

        # Chercher un drone disponible
        available_drone = None
        for drone in drones:
            if drone.is_available() and not drone.is_recharging:
                available_drone = drone
                break  # On prend le premier drone disponible

        if available_drone is None:
            print("No drone available. All drones are either recharging or in use.")
            break

        # Extraire la livraison avec la plus haute priorité
        delivery = heapq.heappop(delivery_heap)

        print(f"Assigning Delivery {delivery.id} to Drone {available_drone.id}")

        # Vérifier que le drone peut effectuer la livraison
        battery_needed = get_battery_needed(available_drone, delivery)
        if available_drone.battery >= battery_needed:  # and add penalty for noflyzone
            start = next(d for d in deliveries if tuple(d.pos) == tuple(available_drone.start_pos))
            goal = next(d for d in deliveries if tuple(d.pos) == tuple(delivery.pos))

            path = a_star(graph, start, goal, no_fly_zones, available_drone, deliveries)

            # Assigner la livraison au drone
            available_drone.move(delivery.pos)

            # Mettre à jour la batterie du drone
            available_drone.update_battery(battery_needed)  # Réduire la batterie utilisée
            delivery.complete()  # Marquer la livraison comme effectuée

            # Marquer le drone comme étant en recharge
            available_drone.start_recharge()

            # Retourner le chemin trouvé
            return path
        else:
            # Si le drone ne peut pas effectuer la livraison, on la remet dans la heap
            print(f"Drone {available_drone.id} doesn't have enough battery for Delivery {delivery.id}. Re-adding to queue.")
            heapq.heappush(delivery_heap, delivery)

        # Simuler une recharge du drone
        for drone in drones:
            drone.decrement_recharge_time()

        # Simuler un tick de temps
        sleep(1)  # Simuler 1 seconde par tick
        tick_count += 1

    if tick_count >= max_ticks:
        print("Simulation reached maximum ticks, stopping.")
