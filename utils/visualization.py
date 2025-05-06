import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def plot_delivery_points(deliveries):
    for delivery in deliveries:
        plt.plot(delivery.pos[0], delivery.pos[1], 'bo', label=f"Delivery {delivery.id}")
    plt.xlabel("X Position (meters)")
    plt.ylabel("Y Position (meters)")
    plt.title("Delivery Points")

def plot_no_fly_zones(no_fly_zones):
    for zone in no_fly_zones:
        polygon = Polygon(zone.coordinates, closed=True, edgecolor='red', facecolor='red', alpha=0.3)
        plt.gca().add_patch(polygon)

def plot_drone_path(path, deliveries, color='green'):
    positions = [deliveries[pt_id].pos for pt_id in path]
    x_vals, y_vals = zip(*positions)
    plt.plot(x_vals, y_vals, color, marker='o', markersize=5, label="Drone Path")

def visualize_scenario(deliveries, no_fly_zones, drone_path=None):
    plt.figure(figsize=(10, 10))

    plot_delivery_points(deliveries)
    plot_no_fly_zones(no_fly_zones)

    if drone_path:
        plot_drone_path(drone_path, deliveries)

    plt.legend(loc='upper left')
    plt.grid(True)
    plt.show()
