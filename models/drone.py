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


        self.current_battery = battery
        self.carrying_weight = 0.0

        self.recharge_time = 0 
        self.is_recharging = False
        self.delivery_in_progress = None 


    def is_available(self):
        return not self.is_recharging

    def start_recharge(self):
        self.is_recharging = True
        self.recharge_time = self.battery * 0.1  # Par exemple 10% du temps de batterie nécessaire pour la recharge

    def decrement_recharge_time(self):
        if self.is_recharging:
            self.recharge_time -= 1
            if self.recharge_time <= 0:
                self.is_recharging = False

    def update_battery(self, amount):
        self.battery -= amount

    def move(self, new_pos):
        self.start_pos = new_pos

    def can_carry(self, weight):
        return weight <= self.max_weight

    def __repr__(self):
        return f"Drone(id={self.id}, pos={self.current_pos}, battery={self.current_battery}mAh)"


