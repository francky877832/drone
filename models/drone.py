class Drone:
    def __init__(self, drone_id, max_weight, battery, speed, start_pos):
        self.id = drone_id
        self.max_weight = max_weight  # in kg
        self.battery = battery        # in mAh
        self.speed = speed            # in m/s
        self.start_pos = start_pos    # tuple (x, y)

        # Internal state
        self.available = True
        self.current_pos = start_pos
        self.current_battery = battery
        self.carrying_weight = 0.0

    def __repr__(self):
        return f"Drone(id={self.id}, pos={self.current_pos}, battery={self.current_battery}mAh)"
