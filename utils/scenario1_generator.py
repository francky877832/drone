import json
import random
from datetime import datetime, timedelta

def random_coord(x_max=100, y_max=100):
    return [random.randint(0, x_max), random.randint(0, y_max)]

def random_time_window():
    start_hour = random.randint(8, 17)
    start = datetime.strptime(f"{start_hour}:00", "%H:%M")
    end = start + timedelta(minutes=30)
    return [start.strftime("%H:%M"), end.strftime("%H:%M")]

# ----- Drones -----
drones = []
for i in range(5):
    drones.append({
        "id": i + 1,
        "max_weight": round(random.uniform(2.0, 5.0), 2),
        "battery": random.randint(8000, 12000),
        "speed": round(random.uniform(8.0, 12.0), 2),
        "start_pos": random_coord()
    })

# ----- Deliveries -----
deliveries = []
for i in range(20):
    deliveries.append({
        "id": 100 + i,
        "pos": random_coord(),
        "weight": round(random.uniform(0.5, 3.0), 2),
        "priority": random.randint(1, 5),
        "time_window": random_time_window()
    })

# ----- No-Fly Zones -----
no_fly_zones = [
    {
        "id": 1,
        "coordinates": [random_coord(), random_coord(), random_coord(), random_coord()],
        "active_time": ["09:30", "09:31"]
    },
    {
        "id": 2,
        "coordinates": [random_coord(), random_coord(), random_coord()],
        "active_time": ["14:00", "14:31"]
    }
]

# ----- Assemble & Save -----
scenario = {
    "drones": drones,
    "deliveries": deliveries,
    "no_fly_zones": no_fly_zones
}

with open("scenario1.json", "w") as f:
    json.dump(scenario, f, indent=4)

print("✅ scenario1.json généré avec succès.")
