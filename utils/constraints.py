from shapely.geometry import LineString, Polygon
from models.drone import Drone
from models.delivery import Delivery
from models.no_fly_zone import NoFlyZone
from utils.helpers import euclidean_distance
from utils.time import is_within_time_window

from datetime import datetime, timedelta






def check_single_delivery_per_trip(drone_assignments):
    for drone_id, deliveries in drone_assignments.items():
        # ici, chaque delivery représente un voyage
        if len(set(deliveries)) != len(deliveries):
            return False
    return True


def check_weight_and_battery(drone: Drone, delivery: Delivery, battery_per_meter=1):
    if delivery.weight > drone.max_weight:
        return False  # surcharge
    distance = euclidean_distance(drone.current_pos, delivery.pos)
    estimated_battery_use = distance * battery_per_meter
    if estimated_battery_use > drone.battery:
        return False
    return True


def intersects_no_fly_zones(start, end, time, no_fly_zones):
    path = LineString([start, end])
    for zone in no_fly_zones:
        if zone.is_active(time):  # à toi de définir cette méthode
            polygon = Polygon(zone.coordinates)
            if path.intersects(polygon):
                return True
    return False


def check_time_window(delivery, delivery_time):
    start = datetime.strptime(delivery.time_window[0], "%H:%M")
    end = datetime.strptime(delivery.time_window[1], "%H:%M")
    return start <= delivery_time <= end



def is_valid_assignment(drone: Drone, delivery: Delivery, current_time, no_fly_zones):
    return (
        check_weight_and_battery(drone, delivery)
        and check_time_window(delivery, current_time)
        and not intersects_no_fly_zones(drone.current_pos, delivery.pos, current_time, no_fly_zones)
    )

def check_constraints(individu, drones, deliveries, no_fly_zones):
    violations = []
    delivery_map = {d.id: d for d in deliveries}
    drone_map = {d.id: d for d in drones}

    drone_time = {f"D{d.id}": datetime.strptime("08:00", "%H:%M") for d in drones}
    drone_pos = {f"D{d.id}": d.current_pos for d in drones}

    for drone_id, assigned_ids in individu.items():
        drone = drone_map[int(drone_id[1:])]  # "D3" → 3
        current_time = drone_time[drone_id]
        current_pos = drone_pos[drone_id]
        battery_used = 0

        for delivery_id in assigned_ids:
            delivery = delivery_map[delivery_id]

            # Vérification du poids
            if delivery.weight > drone.max_weight:
                violations.append(f"Drone {drone_id} en surcharge (> {drone.max_weight} kg) pour livraison {delivery_id}")

            # Calcul distance et consommation
            dist = euclidean_distance(current_pos, delivery.pos)
            battery_used += dist * delivery.weight  # modèle simplifié
            current_pos = delivery.pos

            # Calcul du temps de vol
            speed_m_per_min = (drone.speed * 1000) / 60  # km/h → m/min
            flight_duration = dist / speed_m_per_min
            arrival_time = current_time + timedelta(minutes=flight_duration)

            # Vérification de la plage horaire
            start_time = datetime.strptime(delivery.time_window[0], "%H:%M")
            end_time = datetime.strptime(delivery.time_window[1], "%H:%M")
            if not is_within_time_window(arrival_time, start_time, end_time):
                violations.append(f"Livraison {delivery_id} hors plage horaire ({delivery.time_window})")

            # Vérification No-Fly Zones
            for zone in no_fly_zones:
                zone_start = datetime.strptime(zone.active_time[0], "%H:%M")
                zone_end = datetime.strptime(zone.active_time[1], "%H:%M")
                if zone.contains(delivery.pos) and is_within_time_window(arrival_time, zone_start, zone_end):
                    violations.append(f"Drone {drone_id} entre dans une zone interdite active pour livraison {delivery_id}")

            # Mise à jour du temps courant (+5 minutes de dépôt)
            current_time = arrival_time + timedelta(minutes=5)

        # Vérification batterie
        if battery_used > drone.battery:
            violations.append(f"Drone {drone_id} dépasse la capacité batterie ({battery_used:.1f} > {drone.battery})")

    return (len(violations) == 0), violations






def check_constraints_with_penality(individu, drones, deliveries, no_fly_zones):
    total_penalty = 0  # Toplam ceza
    violated_constraints = []  # Hangi kısıtların ihlal edildiğini sakla

    delivery_map = {d.id: d for d in deliveries}
    drone_map = {d.id: d for d in drones}

    for drone_id, route in individu.items():
        drone = drone_map[int(drone_id[1:])]  # "D3" → 3
        current_pos = drone.current_pos
        current_time = datetime.strptime("08:00", "%H:%M")  # Başlangıç saati

        for delivery_id in route:
            delivery = delivery_map.get(delivery_id)
            if delivery is None:
                total_penalty += 1000
                violated_constraints.append(f"- Teslimat bulunamadı: {delivery_id}")
                continue

            # Mesafe ve tahmini süre
            dist = euclidean_distance(current_pos, delivery.pos)
            duration_minutes = dist / drone.speed * 60
            arrival_time = current_time + timedelta(minutes=duration_minutes)

            # Zaman aralığı kontrolü
            start = datetime.strptime(delivery.time_window[0], "%H:%M")
            end = datetime.strptime(delivery.time_window[1], "%H:%M")
            if not (start <= arrival_time <= end):
                total_penalty += 500
                violated_constraints.append(
                    f"- 🕐 Teslimat {delivery.id} zaman aralığı dışında ({delivery.time_window})"
                )

            # Ağırlık kontrolü
            if delivery.weight > drone.max_weight:
                total_penalty += 1000
                violated_constraints.append(
                    f"- 📦 Teslimat {delivery.id} drone {drone_id} için fazla ağır ({delivery.weight}kg)"
                )

            # Yasak bölge kontrolü
            time_str = arrival_time.strftime("%H:%M")
            for zone in no_fly_zones:
                if zone.is_active(time_str) and zone.contains(delivery.pos):
                    total_penalty += 1000
                    violated_constraints.append(
                        f"- ❌ Teslimat {delivery.id} yasak bölgeye giriyor ({zone.id}) saatte {time_str}"
                    )

            # Sonraki teslimat için pozisyon ve zaman güncelle
            current_pos = delivery.pos
            current_time = arrival_time + timedelta(minutes=1)

    return total_penalty, violated_constraints
