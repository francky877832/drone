import random
from utils.helpers import euclidean_distance, estimate_arrival_time
from utils.time import is_within_time_window


def generate_random_individual(drones, deliveries):
    individual = {f"D{d.id}": [] for d in drones}
    remaining_capacity = {f"D{d.id}": d.max_weight for d in drones}

    shuffled_deliveries = deliveries.copy()
    random.shuffle(shuffled_deliveries)

    for delivery in shuffled_deliveries:
        assigned = False
        random.shuffle(drones)
        for drone in drones:
            key = f"D{drone.id}"
            if remaining_capacity[key] >= delivery.weight:
                individual[key].append(delivery.id)
                remaining_capacity[key] -= delivery.weight
                assigned = True
                break
        if not assigned:
            pass
            #print(f"❗ Livraison {delivery.id} non assignée.")
    return individual


def generate_initial_population(drones, deliveries, size=5):
    return [generate_random_individual(drones, deliveries) for _ in range(size)]


from datetime import datetime, timedelta
import random

def can_assign(drone, delivery, current_time):
    # Ağırlık kontrolü
    if delivery.weight > drone.max_weight:
        return False

    # Zaman aralığı kontrolü
    start = datetime.strptime(delivery.time_window[0], "%H:%M")
    end = datetime.strptime(delivery.time_window[1], "%H:%M")
    current_time = datetime.strptime(drone.start_time, "%H:%M") 

    # Teslimat süresi örnek: 30 dakika
    #delivery_duration = timedelta(minutes=30)

    # Uçuş süresi (km → m, hız: km/h → m/dk)
    distance = euclidean_distance(drone.current_pos, delivery.pos)
    """speed_m_per_min = (drone.speed * 1000) / 60
    flight_time = distance / speed_m_per_min

    # 5 dakika sabit teslimat süresi
    delivery_duration = timedelta(minutes=flight_time + 5)
"""
    arrival_time = estimate_arrival_time(current_time, drone.speed, distance)


    # Drone bu teslimatı bitirdiğinde zaman aralığının içinde mi olacak?
    #print(delivery_duration)
    if not is_within_time_window(arrival_time, start, end):
        return False
    #print("OK")
    return True


def generate_smart_individual(drones, deliveries, start_time="08:00"):
    individual = {f"D{d.id}": [] for d in drones}
    remaining_capacity = {f"D{d.id}": d.max_weight for d in drones}
    drone_time = {f"D{d.id}": datetime.strptime(d.start_time, "%H:%M") for d in drones}  # tous les drones commencent à 08:00

    sorted_deliveries = sorted(deliveries, key=lambda d: d.time_window[0])  # trier par créneau horaire

    for delivery in sorted_deliveries:
        candidate_drones = []
        for drone in drones:
            key = f"D{drone.id}"
            #print(drone_time[key])
            if can_assign(drone, delivery, drone.start_time) and remaining_capacity[key] >= delivery.weight:
                candidate_drones.append(key)

        if candidate_drones:
            chosen_key = random.choice(candidate_drones)
            #let's take the drone
            drone_id = int(chosen_key[1:])  # "D1" → 1
            candidate_drone = next(d for d in drones if d.id == drone_id)

            #print(candidate_drone)
            individual[chosen_key].append(delivery.id) #add a new member to the individu
            remaining_capacity[chosen_key] -= delivery.weight

            #drone_time[chosen_key] += timedelta(minutes=30)  # simulation de temps pris par livraison

            dist = euclidean_distance(candidate_drone.current_pos, delivery.pos)
            speed_m_per_min = (candidate_drone.speed * 1000) / 60  # km/h → m/min
            flight_duration = dist / speed_m_per_min  # durée en minutes

            # Mise à jour de l'heure actuelle du drone
            drone_time[chosen_key] += timedelta(minutes=flight_duration + 5)  # 5 min pour dépôt
            #drones[chosen_key].start_time =  drone_time[chosen_key] #to be done after a delivery

        # Si aucun drone ne peut le prendre, on ignore (ou tu peux le loguer pour debug)

    return individual

def generate_initial_smart_population(drones, deliveries, size=5):
    return [generate_smart_individual(drones, deliveries) for _ in range(size)]

