import json
import random
from datetime import datetime, timedelta

scenario_no = 1

num_drone = 5

num_delivery = 20

delivery_timedelta_hours = 10
delivery_hours_start = 8      # Livraisons commencent à 08:00
delivery_hours_end = 18       # Fin des livraisons à 18:00

num_nfz = 2
nfz_hours_start = 11          # Zones actives de 11h à 12h (heures critiques comme pause déjeuner ou école)
nfz_hours_end = 12
no_fly_zones_vertices = 4     # Carré ou rectangle pour plus de réalisme


drone_min_weight = 2.0        # Minimum réaliste pour petits colis (lettres, médicaments)
drone_max_weight = 8.0        # Max pour colis moyens (nourriture, petits équipements)

drone_min_battery = 5000      # Suffisant pour 2–3 km aller-retour
drone_max_battery = 15000

drone_min_speed = 72.0        # ~20 m/h = 72 km/h, vitesse réaliste pour drone de livraison
drone_max_speed = 216.0        # 60 m/h = 216 km/h, plutôt haut mais possible pour drone très rapide

# Poids des colis à livrer (en kg)
delivery_min_weight = 0.5     # Lettres, médicaments
delivery_max_weight = 5.0     # Petits colis


def random_coord(x_max=100, y_max=100):
    return [random.randint(0, x_max), random.randint(0, y_max)]

def random_time_window():
    start_hour = random.randint(delivery_hours_start, delivery_hours_end)
    start = datetime.strptime(f"{start_hour}:00", "%H:%M")
    end = start + timedelta(hours=delivery_timedelta_hours) #timedelta(minutes=30)
    return [start.strftime("%H:%M"), end.strftime("%H:%M")]

# ----- Drones -----
drones = []
for i in range(num_drone):
    drones.append({
        "id": i + 1,
        "max_weight": round(random.uniform(drone_min_weight, drone_max_battery), 2),
        "battery": random.randint(drone_min_battery, drone_max_battery),
        "speed": round(random.uniform(drone_min_speed, drone_min_speed), 2),
        "start_pos": random_coord(),
        "start_time": "08:00" 
    })

# ----- Deliveries -----
deliveries = []
for i in range(num_delivery):
    deliveries.append({
        "id": 100 + i,
        "pos": random_coord(),
        "weight": round(random.uniform(delivery_min_weight, delivery_max_weight), 2),
        "priority": random.randint(1, num_drone),
        "time_window": random_time_window()
    })

# ----- No-Fly Zones -----

no_fly_zones = []
for i in range(num_nfz):  # Par exemple, 5 zones interdites
    zone = {
        "id": i + 1,
        "coordinates": [random_coord() for _ in range(no_fly_zones_vertices)],
        "active_time": [
            f"{random.randint(nfz_hours_start, nfz_hours_end):02d}:{random.choice(['00', '15', '30', '45'])}",
            f"{random.randint(nfz_hours_start, nfz_hours_end):02d}:{random.choice(['00', '15', '30', '45'])}"
        ]
    }
    no_fly_zones.append(zone)
    

# ----- Assemble & Save -----
scenario = {
    "drones": drones,
    "deliveries": deliveries,
    "no_fly_zones": no_fly_zones
}

with open(f"scenario{scenario_no}.json", "w") as f:
    json.dump(scenario, f, indent=4)

print(f"scenario{scenario_no}.json généré avec succès.")
