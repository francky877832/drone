from datetime import datetime

class Drone:
    def __init__(self, id, max_weight, battery, speed, start_pos, start_time="08:00"):
        self.id = id
        self.max_weight = max_weight
        self.battery = battery
        self.speed = speed
        self.start_pos = start_pos
        self.current_pos = start_pos.copy()
        self.start_time = start_time # datetime.strptime(start_time, "%H:%M")


        # Internal state
        self.available = True
        self.current_pos = start_pos
        self.current_battery = battery
        self.carrying_weight = 0.0

    def can_carry(self, weight):
        return weight <= self.max_weight

    def __repr__(self):
        return f"Drone(id={self.id}, pos={self.current_pos}, battery={self.current_battery}mAh)"


