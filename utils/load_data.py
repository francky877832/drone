def load_data_from_file(file_path):
    drones = []
    deliveries = []
    no_fly_zones = []
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
        drone_section = False
        delivery_section = False
        no_fly_section = False
        
        for line in lines:
            # Skip empty lines or comments
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Start of a new section
            if line.startswith('Drone Data'):
                drone_section = True
                delivery_section = False
                no_fly_section = False
                continue
            if line.startswith('Delivery Data'):
                drone_section = False
                delivery_section = True
                no_fly_section = False
                continue
            if line.startswith('No-Fly Zones Data'):
                drone_section = False
                delivery_section = False
                no_fly_section = True
                continue
            
            # Parse drone data
            if drone_section:
                drone_data = line.split(',')
                drone = {
                    'id': int(drone_data[0]),
                    'max_weight': float(drone_data[1]),
                    'battery': int(drone_data[2]),
                    'speed': float(drone_data[3]),
                    'start_pos': (float(drone_data[4]), float(drone_data[5])),
                }
                drones.append(drone)
            
            # Parse delivery data
            elif delivery_section:
                delivery_data = line.split(',')
                delivery = {
                    'id': int(delivery_data[0]),
                    'pos': (float(delivery_data[1]), float(delivery_data[2])),
                    'weight': float(delivery_data[3]),
                    'priority': int(delivery_data[4]),
                    'time_window': (delivery_data[5], delivery_data[6]),
                }
                deliveries.append(delivery)
            
            # Parse no-fly zone data
            elif no_fly_section:
                no_fly_data = line.split(',')
                no_fly_zone = {
                    'id': int(no_fly_data[0]),
                    'coordinates': [tuple(map(float, coord.strip('()').split(','))) for coord in no_fly_data[1:]],
                }
                no_fly_zones.append(no_fly_zone)
    
    return drones, deliveries, no_fly_zones

# Example usage
drones, deliveries, no_fly_zones = load_data_from_file('../data/sample_data.txt')
