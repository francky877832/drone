import random
from datetime import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.drone import Drone
from models.delivery_point import DeliveryPoint
from models.no_fly_zone import NoFlyZone

# Function to generate random time windows for deliveries
def random_time(start_hour, end_hour):
    h1 = random.randint(start_hour, end_hour - 1)
    h2 = random.randint(h1 + 1, end_hour)
    return (f"{h1:02d}:00", f"{h2:02d}:00")

# Function to generate drones
def generate_drones(num_drones, area_size=(1000, 1000)):
    drones = []
    for i in range(num_drones):
        drone = Drone(
            drone_id=i,
            max_weight=round(random.uniform(2.0, 5.0), 1),
            battery=random.randint(3000, 6000),
            speed=round(random.uniform(5.0, 15.0), 1),
            start_pos=(random.randint(0, area_size[0]), random.randint(0, area_size[1]))
        )
        drones.append(drone)
    return drones

# Function to generate delivery points
def generate_deliveries(num_deliveries, area_size=(1000, 1000)):
    deliveries = []
    for i in range(num_deliveries):
        delivery = DeliveryPoint(
            delivery_id=i,
            pos=(random.randint(0, area_size[0]), random.randint(0, area_size[1])),
            weight=round(random.uniform(0.5, 3.0), 2),
            priority=random.randint(1, 5),
            time_window=random_time(8, 18)
        )
        deliveries.append(delivery)
    return deliveries

# Function to generate no-fly zones
def generate_no_fly_zones(num_zones, area_size=(1000, 1000)):
    zones = []
    for i in range(num_zones):
        x = random.randint(100, area_size[0] - 100)
        y = random.randint(100, area_size[1] - 100)
        width = random.randint(50, 150)
        height = random.randint(50, 150)
        coordinates = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        zone = NoFlyZone(
            zone_id=i,
            coordinates=coordinates,
            active_time=random_time(8, 18)
        )
        zones.append(zone)
    return zones

# Function to generate the complete scenario with drones, deliveries, and no-fly zones
def generate_scenario(num_drones, num_deliveries, num_zones):
    drones = generate_drones(num_drones)
    deliveries = generate_deliveries(num_deliveries)
    zones = generate_no_fly_zones(num_zones)
    return drones, deliveries, zones

# Save the generated data to a sample file (sample_data.txt)
def save_to_file(drones, deliveries, no_fly_zones, filename="data/sample_data.txt"):
    with open(filename, 'w') as f:
        # Writing Drones
        f.write("Drones:\n")
        for drone in drones:
            f.write(f"ID: {drone.id}, Max Weight: {drone.max_weight}, Battery: {drone.battery}, Speed: {drone.speed}, Position: {drone.start_pos}\n")
        
        # Writing Deliveries
        f.write("\nDeliveries:\n")
        for delivery in deliveries:
            f.write(f"ID: {delivery.id}, Position: {delivery.pos}, Weight: {delivery.weight}, Priority: {delivery.priority}, Time Window: {delivery.time_window}\n")
        
        # Writing No-Fly Zones
        f.write("\nNo-Fly Zones:\n")
        for zone in no_fly_zones:
            f.write(f"ID: {zone.id}, Coordinates: {zone.coordinates}, Active Time: {zone.active_time}\n")

# Main function to generate and save a scenario
if __name__ == "__main__":
    num_drones = 5  # Example: 5 drones
    num_deliveries = 10  # Example: 10 deliveries
    num_zones = 3  # Example: 3 no-fly zones

    drones, deliveries, no_fly_zones = generate_scenario(num_drones, num_deliveries, num_zones)
    save_to_file(drones, deliveries, no_fly_zones)
    print(f"Sample data generated and saved to 'data/sample_data.txt'.")
