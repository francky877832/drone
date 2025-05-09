import random
from datetime import datetime, timedelta
from utils.helpers import euclidean_distance, estimate_arrival_time
from utils.time import is_within_time_window


def compute_fitness(individu, drones, deliveries, no_fly_zones, drone_current_time="08:00"):
    delivery_map = {d.id: d for d in deliveries}
    drone_map = {d.id: d for d in drones}
    total_deliveries = 0
    total_energy = 0
    total_violations = 0
    all_violations = []

    for drone_id, assigned_ids in individu.items():
        drone = drone_map[int(drone_id[1:])]
        energy_used = 0

        for delivery_id in assigned_ids:
            delivery = delivery_map[delivery_id]
            violation = False

            # Vérification du poids
            if delivery.weight > drone.max_weight:
                total_violations += 1
                all_violations.append(f"Drone {drone_id} teslimat için aşırı yükü  {delivery_id}")
                violation = True

            # Distance & énergie
            dist = euclidean_distance(drone.current_pos, delivery.pos)
            energy = dist * delivery.weight
            energy_used += energy

            # Estimation de l'heure d'arrivée
            now = estimate_arrival_time(drone.start_time, drone.speed, dist)
            start_time = datetime.strptime(delivery.time_window[0], "%H:%M")
            end_time = datetime.strptime(delivery.time_window[1], "%H:%M")
            #print(delivery_id, " " ,now)
            if not is_within_time_window(now, start_time, end_time):
                total_violations += 1
                all_violations.append(f"Teslimat {delivery_id} zaman aralığı dışında ({delivery.time_window}) - {drone.start_time}")
                violation = True

            # Vérification des No-Fly Zones
            for zone in no_fly_zones:
                zone_start = datetime.strptime(zone.active_time[0], "%H:%M")
                zone_end = datetime.strptime(zone.active_time[1], "%H:%M")
                if zone.contains(delivery.pos) and is_within_time_window(now, zone_start, zone_end):
                    total_violations += 1
                    all_violations.append(f"Drone {drone_id}, teslimat {delivery_id} sırasında yasaklı bölgeye girdi")
                    violation = True

            # Livraison réussie
            if not violation:
                total_deliveries += 1
                drone.current_pos = delivery.pos
                drone.start_time = datetime.strftime(now, "%H:%M")

        # Vérification batterie
        if energy_used > drone.battery:
            total_violations += 1
            all_violations.append(f"Drone {drone_id} pil sınırını aştı ({energy_used:.2f} > {drone.battery})")

        total_energy += energy_used

    # Calcul du fitness
    fitness = (50 * total_deliveries) - (0.1 * total_energy) - (1000 * total_violations)
    return fitness, all_violations
