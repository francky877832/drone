class Drone:
    def __init__(self, id, max_weight, battery, speed, start_pos):
        self.id = id
        self.max_weight = max_weight  # in kg
        self.battery = battery        # in mAh
        self.speed = speed            # in m/s
        self.start_pos = start_pos    # tuple (x, y)
        self.current_pos = start_pos

        # Internal state
        self.available = True
        self.current_pos = start_pos
        self.current_battery = battery
        self.carrying_weight = 0.0

    def can_carry(self, weight):
        return weight <= self.max_weight

    def __repr__(self):
        return f"Drone(id={self.id}, pos={self.current_pos}, battery={self.current_battery}mAh)"


